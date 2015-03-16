import time  
import urllib

def get_ips():
    source_http_ips = "http://www.openbl.org/lists/base_all_http-only.txt"
    list_tor_ips    = list()

    data = urllib.urlopen(source_http_ips)
    for line in data:
        if line[:1] != "#":
            entry = [line.rstrip(), 'BLOCK', 'HTTP Scan', int(time.time())]
            list_tor_ips.append(entry);

    return list_tor_ips

def get_description():
    return 'HTTP Scan'

def get_refresh_rate():
    return 3600
