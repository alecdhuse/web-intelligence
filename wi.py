import plugin_http_scans as http_scans
import plugin_tor as tor
import pymysql

ip_list  = list();
ip_count = 0

#Import TOR Exit Nodes
#tor_node_list = tor.get_ips()
#ip_count += len(tor_node_list)
#ip_list.append(tor_node_list)

#Import HTTP Malicous Scans
#http_scans_list = http_scans.get_ips()
#ip_count += len(http_scans_list)
#ip_list.append(tor_node_list)

db_host = "localhost"
db_port = 3306
db_user = "foldingm_intel"
db_pass = "7wl2RMOEoAEj5ya4"
db_db   = "foldingm_intelligence"

conn = pymysql.connect(db_host, db_port, db_user, db_pass, db_db)
cur = conn.cursor()
cur.execute("SELECT * FROM IP_List")
print(cur.timestamp)
for row in cur:
   print(row)


cur.close()
conn.close()

print "Imported Items: " + str(ip_count)
