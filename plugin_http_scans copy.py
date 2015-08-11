import urllib2

def get_ips():
    source_http_ips = "http://www.openbl.org/lists/base_all_http-only.txt"
    api_url         = "http://topohawk.com/api/v1/update_ip_list.php"
    list_tor_ips    = list()

    data = urllib2.urlopen(source_http_ips)
    for line in data:
        if line[:1] != "#":
            user_ip = line.rstrip()
            request = urllib2.Request(api_url, urllib.urlencode({'key':'TuZtKHDCzj8x4Jww2RAp', 'ip': user_ip, 'action':'BLOCK', 'description':'HTTP Scan'}))
            handler = urllib2.urlopen(request)
            response = handler.read();

get_ips()
