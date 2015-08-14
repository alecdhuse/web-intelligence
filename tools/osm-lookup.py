import json
from nominatim import Nominatim, NominatimReverse
import time
import urllib, urllib2

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

country_codes = "https://raw.githubusercontent.com/alecdhuse/web-intelligence-data/master/country_codes.json"
level2_divisions = "https://raw.githubusercontent.com/alecdhuse/web-intelligence-data/master/level-2-divisions.json"
source = "https://raw.githubusercontent.com/alecdhuse/web-intelligence-data/master/university_networks.json"
nominatim = Nominatim()

# Load country codes
cc_data = urllib2.urlopen(country_codes)
country_codes_json = json.load(cc_data)

# Load level 2 divisions
lvl2_data = urllib2.urlopen(level2_divisions)
level2_divisions_json = json.load(lvl2_data)

# Load source data
data = urllib2.urlopen(source)
json_data = json.load(data)

for entry in json_data['universities']:
    uni_name = entry['name']

    if not ('osm' in entry):
        result = nominatim.query(uni_name)
        country_index = 5
        level2_index = 4
        found_country = False
        found_level2  = False
        
        if (len(result) == 1):
            display_name = result[0]['display_name'].split(',')

            if (len(display_name) >= 6):
                obj_name = display_name[0].strip()
                obj_city = display_name[2].strip()
                obj_code = display_name[5].strip() 
                obj_lon  = result[0]['lon']
                obj_lat  = result[0]['lat']
            else:
                print "Error with " + result[0]['display_name']
                pass

            while found_country == False:
                if (country_index < len(display_name)):
                    obj_cnty = display_name[country_index].strip().split('/')[0]
                     
                    if (obj_cnty in country_codes_json['countries']):
                        obj_cc = country_codes_json['countries'][obj_cnty]['ISO 3166-1 alpha-2']
                        found_country = True
                        break
                    else:
                        country_index += 1
                else:
                    print "Country error"
                    print "\tDisplay name: " + result[0]['display_name']
                    print "\tUniversity Name: " + uni_name
                    found_country = False
                    break

            if (found_country == True):
                level2_index = country_index - 1

                # Verify level 2 division
                while found_level2 == False:
                    if (level2_index > 0):
                        obj_level2 = display_name[level2_index].strip()

                        if (obj_level2 in level2_divisions_json['divisions']):
                            found_level2 = True
                            break;
                        else:
                            obj_level2 = "?"
                            level2_index = level2_index - 1
                    else:
                        obj_level2 = "?"
                        found_level2 = False
                        break

                # Verify postal code
                if (object_cc == "US"):
                    if not is_int(obj_code):
                        obj_code = ""
                        
                        for token in display_name
                            if is_int(token.strip()) and len(token.strip()) == 5:
                                obj_code = oken.strip()
                                break
                        
                for network in entry['networks']:
                    network['country'] = obj_cc
                    network['city'] = obj_city
                    network['division'] = obj_level2
                    network['code'] = obj_code
                    network['lng'] = float(obj_lon)
                    network['lat'] = float(obj_lat)

                entry['osm'] = True
                print "Updated info for " + uni_name
                
        elif (len(result) > 1):
            print "Too many results for " + uni_name
            entry['osm'] = True
        else:
            print "No results for " + uni_name
            entry['osm'] = True

        time.sleep(11)

        with open('data.txt', 'w') as outfile:
            json.dump(json_data, outfile)
