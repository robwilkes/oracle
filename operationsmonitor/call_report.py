from libpalladion.scripting.Model import Call, Device
from libpalladion.utils.logsys import debug, info, error
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

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

def concat_devices(call_devices,sys_devices):
	if not call_devices is None:
		results = []
		deviceids = call_devices.split(",")
		for deviceid in deviceids:
			results.append(sys_devices[deviceid]['name'])
		return ",".join(results)

def convert_plus_e164(phone_number):
	if not phone_number is None:
		result = phone_number
		result = re.sub('^0([2-9]\d{8})', '+61\g<1>', result)
		result = re.sub('^(61[2-9]\d{8})', '+\g<1>', result)
		return result
	else:
		return None

def call_type(caller, callee, pai):
	if caller is None and not pai is None:
		caller = pai
	if re.search('^\+614\d{8}', caller) or re.search('^\+614\d{8}', callee):
		return 'Mobile'
	elif re.search('^\+612\d{8}', caller) and re.search('^\+612\d{8}', callee):
		return 'State'
	elif re.search('^\+613\d{8}', caller) and re.search('^\+613\d{8}', callee):
		return 'State'
	elif re.search('^\+617\d{8}', caller) and re.search('^\+617\d{8}', callee):
		return 'State'
	elif re.search('^\+618\d{8}', caller) and re.search('^\+618\d{8}', callee):
		return 'State'
	elif re.search('^\+612\d{8}', caller) and re.search('^\+61[3,7,8]\d{8}', callee):
		return 'National'
	elif re.search('^\+613\d{8}', caller) and re.search('^\+61[2,7,8]\d{8}', callee):
		return 'National'
	elif re.search('^\+617\d{8}', caller) and re.search('^\+61[2,3,8]\d{8}', callee):
		return 'National'
	elif re.search('^\+618\d{8}', caller) and re.search('^\+61[2,3,7]\d{8}', callee):
		return 'National'
	elif re.search('^\+61000', callee):
		return 'Emergency'
	elif re.search('^\+6113\d{4}', callee) or re.search('^\+6113\d{6}', callee) or re.search('^\+6118\d{6}', callee):
		return 'Toll Free'
	elif re.search('^\+61190\d{7}', callee):
		return 'Premium'
	else:
		return 'International/Other'


#
# Script entry point
#

def run(facade, args):
	# Check parameters
	end_ts = datetime.utcnow()
	start_ts = end_ts - relativedelta(days=int(args["days"])) - relativedelta(weeks=int(args["weeks"])) - relativedelta(months=int(args["months"]))
	
	info('From Timestamp (UTC): {}'.format(start_ts))
	info('To   Timestamp (UTC): {}'.format(end_ts))

	devices = {}

	for dev in [dev for dev in facade.getDevices()]:
		devices[str(dev.id)] = {'name': str(dev.name)}

	for call in facade.getCalls(filter=[Call.setup_start_ts >= start_ts, 
										Call.setup_start_ts <= end_ts]):

		if not call.state_msg == "Established" and \
		not call.state_msg == "Proceeding" and \
		not call.state_msg == "Ringing":
			mos_avg = call.MOSlqe_avg if not call.MOSlqe_avg == None else 0.00

			facade.addResult({  'callid': get_callid(call),
								'caller': convert_plus_e164(call.src_user),
								'callee': convert_plus_e164(call.dst_user),
								'start_timestamp': call.setup_start_ts,
								'end_timestamp': call.end_ts,
								'duration(sec)': convert_ms2s(call.call_time),
								'code': call.code,
								'ingress': concat_devices(call.ingress_devs, devices),
								'egress': concat_devices(call.egress_devs, devices),
								'pai': convert_plus_e164(call.pai),
								'mos_avg': '{:.2f}'.format(mos_avg),
								'state': call.state_msg,
								'type': call_type(convert_plus_e164(call.src_user), convert_plus_e164(call.dst_user), convert_plus_e164(call.pai))
				})