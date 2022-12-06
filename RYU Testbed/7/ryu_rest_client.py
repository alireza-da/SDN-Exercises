#! /usr/bin/env python3 
# -*- coding: utf-8 -*-

import requests 
import json 

ip_address = '127.0.0.1' 
port = '8080' 
rest_path = '/simpleswitch/mactable' 
switch = '0000000000000001' 
pad = 15

# Get the JSON output from the RESTful API 
url = 'http://{}:{}{}/{}'.format(ip_address, port, rest_path, switch)

response = requests.get(url) 
response_bytes = response.content 
response_str = response_bytes.decode('utf-8') 

if (response.ok): 
    json_dict = json.loads(response_str) 
else: 
    print('There has been a problem connecting to REST API') 
    exit(1) 

# Print equivalent 'curl' command 
heading = 'Equivalent CURL command to interact with server from server' 
print('\n{}'.format(heading)) 
print('-' * len(heading),'\n') 
print(' $ curl {}'.format(url)) 

# Print out the naked list received 
heading = 'Naked JSON list received from server' 
print('\n{}'.format(heading)) 
print('-' * len(heading),'\n')
print(json_dict) 

# Breakdown list into individual element pairs 
heading = 'Breakdown list into individual element pairs' 
print('\n{}'.format(heading)) 
print('-' * len(heading),'\n') 

print ('MAC address {} Port'.format(' ' * 7)) 
print ('{} {} {}'.format('-' * 11, ' ' * 7, '-' * 4)) 
print() 

for mac in sorted(json_dict.keys()): 
    pad_digits = pad - len(mac) 
    print('{} {} {}'.format(mac, ' ' * pad_digits, json_dict[mac]))
    

# End of Program