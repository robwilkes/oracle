from libpalladion.scripting.Model import Call, Device
from libpalladion.utils.logsys import debug, info, error
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def convert_ms2s(ms):
    if not ms is None:
        return int(ms/1000)
    else:
        return 0

def avg_as_string(mos_sum, call_total):
    if not call_total is None and not call_total == 0:
        return '{:.2f}'.format(mos_sum/call_total)
    else:
        return '{:.2f}'.format(0)

#
# Script entry point
#

def run(facade, args):
    # Check parameters
    end_ts = datetime.utcnow()
    start_ts = end_ts - relativedelta(days=int(args["days"])) - relativedelta(weeks=int(args["weeks"]))

    info('From Timestamp (UTC): {}'.format(start_ts))
    info('To   Timestamp (UTC): {}'.format(end_ts))

    devices = {}
    calllog = []

    for dev in [dev for dev in facade.getDevices()]:
        devices[str(dev.id)] = {'name': str(dev.name), 'concurrent': 0, 'peak': 0, 'total': 0}

    info('Device List')
    info('ID\tName')
    for key, value in devices.items():
        info('{}\t{}'.format(key, value.get('name')))

    for call in facade.getCalls(filter=[Call.setup_start_ts >= start_ts,
                                        Call.setup_start_ts <= end_ts,
                                        Call.state_msg == "Finished",
                                        Call.code == 200]):

        call_start = call.setup_start_ts
        call_end = call_start + timedelta(seconds=convert_ms2s(call.call_time))
        mos_avg = call.MOSlqe_avg if not call.MOSlqe_avg == None else 4.41

        if not call.ingress_devs is None:
            calllog.append({
                'deviceid': call.ingress_devs,
                'timestamp':call_start.strftime('%Y/%m/%d %H:%M:%S'),
                'mos_avg': mos_avg,
                'state':'start'
            })
            calllog.append({
                'deviceid': call.ingress_devs,
                'timestamp':call_end.strftime('%Y/%m/%d %H:%M:%S'),
                'mos_avg': mos_avg,
                'state':'finish'
            })

        if not call.egress_devs is None:
            calllog.append({
                'deviceid': call.egress_devs,
                'timestamp':call_start.strftime('%Y/%m/%d %H:%M:%S'),
                'mos_avg': mos_avg,
                'state':'start'
            })
            calllog.append({
                'deviceid': call.egress_devs,
                'timestamp':call_end.strftime('%Y/%m/%d %H:%M:%S'),
                'mos_avg': mos_avg,
                'state':'finish'
            })

    results = {}

    for call in sorted(calllog, key=lambda k: k['timestamp']):
        deviceid = call['deviceid'].split(',')[0]
        cuc = devices[deviceid]['name'].split('-')[0]

        if not cuc in results:
            results[cuc] = {'concurrent': 0, 'peak': 0, 'total': 0, 'mos_sum': 0}

        if call['state'] == 'start':
            results[cuc]['concurrent'] += 1
            results[cuc]['total'] += 1
            results[cuc]['mos_sum'] += call['mos_avg']
        elif call['state'] == 'finish':
            results[cuc]['concurrent'] -= 1

        if results[cuc]['concurrent'] > results[cuc]['peak']:
            results[cuc]['peak'] = results[cuc]['concurrent']

    results2 = []
    for key, cuc in results.items():
        results2.append({
            'cuc': key,
            'total': cuc['total'],
            'peak': cuc['peak'],
            'mos_avg': avg_as_string(cuc['mos_sum'], cuc['total'])
        })
    
    for result in sorted(results2, key=lambda k: k['peak'], reverse=True):
        facade.addResult({
            'cuc': result['cuc'],
            'total': result['total'],
            'peak': result['peak'],
            'mos_avg': result['mos_avg']
        })
