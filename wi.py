import plugin_http_scans as http_scans
import plugin_tor as tor

ip_list  = list();
ip_count = 0

#Import TOR Exit Nodes
tor_node_list = tor.get_ips()
ip_count += len(tor_node_list)
ip_list.append(tor_node_list)

#Import HTTP Malicous Scans
http_scans_list = http_scans.get_ips()
ip_count += len(http_scans_list)
ip_list.append(tor_node_list)

print "Imported Items: " + str(ip_count)
