import time  
import urllib

def get_ips():
    source_http_ips = "http://www.openbl.org/lists/base.txt"
    list_tor_ips    = list()

    data = urllib.urlopen(source_http_ips)
    for line in data:
        if line[:1] != "#":
            entry = [line.rstrip(), 'BLOCK', 'RBL', int(time.time())]
            list_tor_ips.append(entry);

    return list_tor_ips

def get_description():
    return 'HTTP Scan'

def get_refresh_rate():
    return 3600
