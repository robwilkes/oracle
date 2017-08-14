from libpalladion.scripting.Model import Call, Device
from libpalladion.utils.logsys import debug, info, error

def match_device(cl,ml,d):
    if ml == "ANY":
        return True
    elif not cl == None:
        for c in cl.split(","):
            for m in ml:
                if m in d.get(c):
                    return True

def concat_devices(cl,d):
    c = cl.split(",")
    return d.get(c[0])

def convert_ms2s(ms):
    if ms == None:
        return None
    else:
        return ms/1000

#
# Script entry point
#

def run(facade, args):
    # Check parameters
    start_ts = args.get("start_ts")
    end_ts = args.get("end_ts")

    try:
        ingress_devices = [n.strip().upper() for n in args["ingress_devs"].split(",")]
    except:
        ingress_devices = "ANY"

    try:
        egress_devices = [n.strip().upper() for n in args["egress_devs"].split(",")]
    except:
        egress_devices = "ANY"

    devices = {}; devs = facade.getDevices()

    for dev in devs:
        devices.update({str(dev.id):str(dev.name)})

    for call in facade.getCalls(filter=[Call.setup_start_ts >= start_ts,
                                        Call.setup_start_ts <= end_ts]):

        if match_device(call.ingress_devs, ingress_devices, devices) and match_device(call.egress_devs, egress_devices, devices):
            facade.addResult({  'caller': call.src_user,
                                'callee': call.dst_user,
                                'timestamp': call.setup_start_ts,
                                'duration(sec)': convert_ms2s(call.call_time),
                                'code': call.code,
                                'state': call.state_msg,
                                'ingress': concat_devices(call.ingress_devs, devices),
                                'egress': concat_devices(call.egress_devs, devices)
            })