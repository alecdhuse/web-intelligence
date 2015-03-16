import ipaddr
import json
import time  
import urllib2

def get_networks():
    source_networks = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    test_networks = "http://topohawk.com/t1/ip-ranges.json"
    networks_list = list()

    data = urllib2.urlopen(test_networks)
    json_data = json.load(data)   
    networks_json = json_data["prefixes"]

    for network_entry in networks_json:
        ip_network = ipaddr.IPNetwork(network_entry["ip_prefix"])
        first_ip = ""
        last_ip = ""
        
        for ip in ip_network.iterhosts():
            if first_ip == "":
                first_ip = ip

            last_ip = ip
            pass

        list.append(first_ip, last_ip, 'READONLY', 'Amazon AWS', int(time.time())])

    return list

def get_description():
    return 'Amazon Networks'

def get_refresh_rate():
    return 86400

get_networks()
