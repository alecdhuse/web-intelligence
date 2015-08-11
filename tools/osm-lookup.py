import json
from nominatim import Nominatim, NominatimReverse
import time
import urllib, urllib2

country_codes = "https://raw.githubusercontent.com/alecdhuse/web-intelligence-data/master/country_codes.json"
source = "https://raw.githubusercontent.com/alecdhuse/web-intelligence-data/master/university_networks.json"
nominatim = Nominatim()

# Load country codes
cc_data = urllib2.urlopen(country_codes)
country_codes_json = json.load(cc_data)

# Load source data
data = urllib2.urlopen(source)
json_data = json.load(data)

for entry in json_data['universities']:
    uni_name = entry['name']

    if not ('osm' in entry):
        result = nominatim.query(uni_name)

        if (len(result) == 1):
            display_name = result[0]['display_name'].split(',')
            obj_name = display_name[0].strip()
            obj_city = display_name[2].strip()
            obj_div  = display_name[4].strip()
            obj_code = display_name[5].strip()
            obj_cnty = display_name[6].strip()
            obj_lon  = result[0]['lon']
            obj_lat  = result[0]['lat']

            if (obj_cnty in country_codes_json['countries']):
                obj_cc = country_codes_json['countries'][obj_cnty]['ISO 3166-1 alpha-2']

                for network in entry['networks']:
                    network['country'] = obj_cc
                    network['city'] = obj_city
                    network['division'] = obj_div
                    network['code'] = obj_code
                    network['lng'] = float(obj_lon)
                    network['lat'] = float(obj_lat)

                entry['osm'] = True
                print "Updated info for " + uni_name
            else:
                print "Country error for " + obj_cnty
                print "\tDisplay name: " + display_name
                print "\tUniversity Name: " + uni_name
                
        elif (len(result) > 1):
            print "Too many results for " + uni_name
            entry['osm'] = True
        else:
            print "No results for " + uni_name
            entry['osm'] = True

        time.sleep(11)

        with open('data.txt', 'w') as outfile:
            json.dump(json_data, outfile)
