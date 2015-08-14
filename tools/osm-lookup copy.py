import json
import time
import urllib, urllib2


postal_codes = "https://raw.githubusercontent.com/alecdhuse/web-intelligence-data/master/us_postal_codes.json"
pc_data = urllib2.urlopen(postal_codes)
new_data = []
entries = {}

for line in pc_data:
    line_json = json.loads(line)
    new_entry_data = {"city" : line_json['city'], "state" : line_json['state']}
    entries[line_json['_id']] = new_entry_data

#new_data.append(new_entry)

with open('data-codes.txt', 'w') as outfile:
    json.dump(entries, outfile)
