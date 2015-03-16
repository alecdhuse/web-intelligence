import time  
import urllib

def get_ips():
    source_tor_ips  = "https://www.dan.me.uk/torlist/"
    source_tor_test = "https://topohawk.com/t1/torlist.txt"
    list_tor_ips    = list()

    data = urllib.urlopen(source_tor_test)
    for line in data:
        entry = [line.rstrip(), 'READONLY', 'TOR Exit Node', int(time.time())]
        list_tor_ips.append(entry);

    return list_tor_ips

def get_description():
    return 'TOR Exit Node'

def get_refresh_rate():
    return 2400
