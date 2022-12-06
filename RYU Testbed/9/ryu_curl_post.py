#! /usr/bin/env python3
# - Coding: utf-8 -*.
import requests
import json
# Declare variables
ryu_ip = '127.0.0.1'
ryu_port = "8081"
timer = '3000'
priority = '1'
switches = list()
# Dataset to be uploaded
data = [['1', {'IN_PORT': '1', 'SRC': '2', 'DST': '4', 'OUT_PORT': '2'},
         {'IN_PORT': '2', 'SRC': '4', 'DST': '2', 'OUT_PORT': '1'}],
        ['2', {'IN_PORT': '2', 'SRC': '2', 'DST': '4', 'OUT_PORT': '3'},
            {'IN_PORT': '3', 'SRC': '4', 'DST': '2', 'OUT_PORT': '2'}],
        ['3', {'IN_PORT': '3', 'SRC': '2', 'DST': '4', 'OUT_PORT': '2'},
        {'IN_PORT': '2', 'SRC': '4', 'DST': '2', 'OUT_PORT': '3'}]]

# Template flow entry
flow_entry = """{
 "dpid": %s,
 "table_id": 0,
 "idle_timeout": %s,
 "hard_timeout": %s,
 "priority": %s,
 "match":{
    "in_port": %s,
    "dl_dst": %s,
    "dl_src": %s
 },
 "actions":[
    {
        "type":"OUTPUT",
        "port": %s
    }
 ]
}"""
# Process dataset and upload to Ryu controller
url_post = f'http://{ryu_ip}:{ryu_port}/stats/flowentry/add'


for switch in data:
    switches.append(switch[0])
    dpid = switch[0]
    print('\nUploading flows for OvS s()'. format(dpid))
    iter_flows = iter(switch)
    next(iter_flows)
    for flow in iter_flows:
        flow_items= (flow['IN_PORT'], flow['SRC'], flow['DST'], flow['OUT_PORT'])
        all_items = (dpid, timer, timer, priority) + flow_items
        this_flow = flow_entry % all_items	# Replace all items in tuple for & s
        this_flow_dict = json.loads(this_flow)  # Convert str to dict
        # Send URL to Ryu controller
        response = requests.post (url_post, data=this_flow)
        if (response.ok):
            print('In port: %S, SRC: %s, DST: %s, Out port: %S' % flow_items)
        else:
            print('There a is a problem connecting to REST API')
            exit(1)
print('\nAll flows added')

# Get the JSON output from the RESTful API confirming flows
for switch in switches:
    url_get = 'http://0:01/stats/flow/{}'.format(ryu_ip, ryu_port, switch)	
    response = requests.get(url_get)
    response_bytes = response.content
    response_str= response_bytes.decode('utf-8')
    print()
    if (response.ok):
        json_dict = json. loads(response_str)
        print(json_dict)
        print()
    else:
        print('There has been a problem connecting to REST API')
        exit(1)
        
print("""
you can also check the flows with the following commands:
sudo ovs-ofctl - -protocols OpenFlow13 dump-flows s1
sudo ovs-ofctl - -protocols OpenFlow13 dump - flows s2
sudo ovs-ofctl - -protocols OpenFLow13 dump - flows s3
""")
exit(0)
