from libpalladion.scripting.Model import Call, Device
from libpalladion.utils.logsys import debug, info, error
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def convert_ms2s(ms):
	if not ms is None:
		return int(ms/1000)
	else:
		return 0

def get_callid(call):
	for leg in call.getLegs():
		if not leg.callid is None:
			return leg.callid
	return None

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
		devices[str(dev.id)] = {'name': str(dev.name), 'concurrent': 0, 'peak': 0, 'total': 0, 'mos_sum': 0}

	for call in facade.getCalls(filter=[Call.setup_start_ts >= start_ts, 
										Call.setup_start_ts <= end_ts, 
										Call.state_msg == "Finished",
										Call.code == 200]):

		call_start = call.setup_start_ts
		call_end = call_start + timedelta(seconds=convert_ms2s(call.call_time))
		mos_avg = call.MOSlqe_avg if not call.MOSlqe_avg == None else 4.41

		if not call.ingress_devs is None:
			calllog.append({'deviceid': call.ingress_devs, 'timestamp':call_start.strftime('%Y/%m/%d %H:%M:%S'), 'callid': get_callid(call), 'mos_avg': mos_avg, 'state':'start'})
			calllog.append({'deviceid': call.ingress_devs, 'timestamp':call_end.strftime('%Y/%m/%d %H:%M:%S'), 'callid': get_callid(call), 'mos_avg': mos_avg, 'state':'finish'})

		if not call.egress_devs is None:
			calllog.append({'deviceid': call.egress_devs, 'timestamp':call_start.strftime('%Y/%m/%d %H:%M:%S'), 'callid': get_callid(call), 'mos_avg': mos_avg, 'state':'start'})
			calllog.append({'deviceid': call.egress_devs, 'timestamp':call_end.strftime('%Y/%m/%d %H:%M:%S'), 'callid': get_callid(call), 'mos_avg': mos_avg, 'state':'finish'})

	for call in sorted(calllog, key=lambda k: k['timestamp']):
		deviceid = call['deviceid']
		if call['state'] == 'start':
			devices[deviceid]['concurrent'] += 1
			devices[deviceid]['total'] += 1
			devices[deviceid]['mos_sum'] += call['mos_avg']
		elif call['state'] == 'finish':
			devices[deviceid]['concurrent'] -= 1

		if devices[deviceid]['concurrent'] > devices[deviceid]['peak']:
			devices[deviceid]['peak'] = devices[deviceid]['concurrent']

	results = []
	for key, device in devices.iteritems():
		results.append({'device': device['name'], 'total': device['total'], 'peak': device['peak'], 'mos_avg': avg_as_string(device['mos_sum'], device['total'])})
	
	for device in sorted(results, key=lambda k: k['peak'], reverse=True):
		facade.addResult({'device': device['device'], 'total': device['total'], 'peak': device['peak'], 'mos_avg': device['mos_avg']})
