from libpalladion.scripting.Model import Call, Device
from libpalladion.utils.logsys import debug, info, error
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def match_device(idevs,edevs,cdev):
    if not idevs is None:
        if cdev in idevs:
            return True

    if not edevs is None:
        if cdev in edevs:
            return True
    
    return False

def convert_ms2s(ms):
    if ms is None:
        return None
    else:
        return ms/1000

def get_callid(call):
    for leg in call.getLegs():
        if not leg.callid is None:
            return leg.callid
    return None

def concat_devices(cl,d):
    if not cl is None:
        devices = []
        c = cl.split(",")
        for o in c:
            devices.append(d.get(o))
        return ",".join(devices)

#
# Script entry point
#

def run(facade, args):
    # Check parameters
    end_ts = datetime.utcnow()
    start_ts = end_ts - relativedelta(days=int(args["days"])) - relativedelta(weeks=int(args["weeks"]))
    
    info('From Timestamp (UTC): {}'.format(start_ts))
    info('To   Timestamp (UTC): {}'.format(end_ts))

    total = 0
    concurrent = 0
    peak = 0

    customer = args["customer"].upper()

    devices = {}
    statelist = []
    state = {}

    for dev in [dev for dev in facade.getDevices()]:
        devices.update({str(dev.id):str(dev.name)})

    for call in facade.getCalls(filter=[Call.setup_start_ts >= start_ts, Call.setup_start_ts <= end_ts, Call.code == 200]):

        if match_device(concat_devices(call.ingress_devs, devices), concat_devices(call.egress_devs, devices), customer) \
            and not call.state_msg == "Established" \
            and not call.state_msg == "Proceeding":
            facade.addResult({  'callid': get_callid(call),
                                'caller': call.src_user,
                                'callee': call.dst_user,
                                'timestamp': call.setup_start_ts,
                                'duration(sec)': convert_ms2s(call.call_time),
                                'code': call.code,
                                'state': call.state_msg,
                                'ingress': concat_devices(call.ingress_devs, devices),
                                'egress': concat_devices(call.egress_devs, devices)
            })