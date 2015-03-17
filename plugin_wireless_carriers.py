#!/usr/bin/python
import ipaddr
import json
import MySQLdb
import socket
import struct
import time  
import urllib2

def get_networks():
    source_networks = "https://raw.githubusercontent.com/scarlet-shark/web-intelligence-data/master/mobile_networks_north-america.json"
    networks_list = list()

    data = urllib2.urlopen(source_networks)
    json_data = json.load(data)   
    networks_json = json_data["networks"]

    for network_entry in networks_json:
        for network_group in network_entry["networks"]:
            networks_list.append([network_group["start"], network_group["end"], 'FULL', get_description(), int(time.time())])

    print networks_list
    return networks_list

def get_description():
    return 'Wireless Carrier Networks'

def get_refresh_rate():
    return 1000000

def ip2long(ip):
    """
    Convert an IP string to long
    """
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

get_networks()
