from libpalladion.scripting.Model import Call, Device
from libpalladion.utils.logsys import debug, info, error
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def match_device(cl,ml,d):
    if ml == "ANY":
        return True
    elif not cl is None:
        for c in cl.split(","):
            for m in ml:
                if m in d.get(c):
                    return True
    else:
        return False

def match_responsecodes(c,ml):
    if ml == "ANY":
        return True
    elif str(c) in ml:
        return True
    else:
        return False

def concat_devices(cl,d):
    if not cl is None:
        devices = []
        c = cl.split(",")
        for o in c:
            devices.append(d.get(o))
        return ",".join(devices)

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

#
# Script entry point
#

def run(facade, args):
    # Check parameters
    start_ts = datetime.today() - relativedelta(days=int(args["days"])) - relativedelta(weeks=int(args["weeks"])) - relativedelta(months=int(args["months"]))
    end_ts = datetime.today()

    if args["ingress_devs"].upper() == "*" or args["ingress_devs"].upper() == "ANY":
        ingress_devices = "ANY"
    else:
        ingress_devices = [n.strip().upper() for n in args["ingress_devs"].split(",")]

    if args["egress_devs"].upper() == "*" or args["egress_devs"].upper() == "ANY":
        egress_devices = "ANY"
    else:
        egress_devices = [n.strip().upper() for n in args["egress_devs"].split(",")]

    if args["response_codes"].upper() == "*" or args["response_codes"].upper() == "ANY":
        response_codes = "ANY"
    else:
        response_codes = [n.strip().upper() for n in args["response_codes"].split(",")]

    devices = {}; devs = facade.getDevices()

    for dev in devs:
        devices.update({str(dev.id):str(dev.name)})

    for call in facade.getCalls(filter=[Call.setup_start_ts >= start_ts,
                                        Call.setup_start_ts <= end_ts]):

        if match_device(call.ingress_devs, ingress_devices, devices) and \
        match_device(call.egress_devs, egress_devices, devices) and \
        match_responsecodes(call.code, response_codes) and\
        not call.state_msg == "Established" and\
        not call.state_msg == "Proceeding":
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