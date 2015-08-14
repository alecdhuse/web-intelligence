import json
from nominatim import Nominatim, NominatimReverse
import time
import urllib, urllib2

class Object_info:
    country = ""
    lvl2_div = ""
    city = ""
    post_code = ""
    lat = 0
    lng = 0

    def __init__(self):
        self.country = ""
        self.lvl2_div = ""
        self.city = ""
        self.post_code = ""
        self.lat = 0
        self.lng = 0

    def __str__(self):
        return self.country + ", " + self.lvl2_div + ", " + self.city + ", " + self.post_code
        
    def __repr__(self):
        return self.__str__()
    
def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def parse_object_info(info_string):
    info_tokens = info_string.split(',')
    obj_info = Object_info()
    found_country = False
    found_lvl2_div = False
    found_postal_code = False
    
    for token in reversed(info_tokens):
        if found_country == False:
            if (token.strip() in country_codes_json['countries']):
                obj_info.country = country_codes_json['countries'][token.strip()]['ISO 3166-1 alpha-2']
                found_country = True
                pass

        if found_lvl2_div == False:
            if (token.strip() in level2_divisions_json['divisions']):
                if found_country == True:
                    if obj_info.country in level2_divisions_json['divisions'][token.strip()]:
                        # Country code is listed as having this level 2 division
                        obj_info.lvl2_div = token.strip()
                        found_lvl2_div = True
                        pass
                    else:
                        print "\tlvl2 div error"
                        print "\t" + level2_divisions_json['divisions'][token.strip()]
                else:
                    obj_info.lvl2_div = token.strip()
                    found_lvl2_div = True
                    pass

        if found_postal_code == False:
            if found_country == True:
                if obj_info.country == "US":
                    if is_int(token.strip()):
                        if token.strip() in postal_code_json:
                            obj_info.post_code = token.strip()
                            obj_info.city = postal_code_json[token.strip()]['city'].title().strip()
                            found_postal_code = True

                            if len(obj_info.lvl2_div) == 0:
                                obj_info.lvl2_div = postal_code_json[token.strip()]['state']
                        elif len(token.strip()) == 5:
                            print "*\tUnkown Postal Code: " + token.strip()
                            print "**\t" + info_string
                    
                elif obj_info.country == "CA":
                    if token.strip() in postal_code_json_ca:
                            obj_info.post_code = token.strip()
                            obj_info.city = postal_code_json_ca[token.strip()]['city'].title().strip()
                            found_postal_code = True
                    else:
                            print "*\tUnkown Postal Code: " + token.strip()
                            print "**\t" + info_string
                            
                elif obj_info.country == "NZ":
                    if token.strip() in postal_code_json_nz:
                            obj_info.post_code = token.strip()
                            obj_info.city = postal_code_json_nz[token.strip()]['city'].title().strip()
                            found_postal_code = True
                    else:
                            print "*\tUnkown Postal Code: " + token.strip()
                            print "**\t" + info_string                    
                else:
                    print "*\tPostal code format for " + obj_info.country + " not known."
                    print "**\t" + info_string
        
    return obj_info

country_codes = "https://raw.githubusercontent.com/alecdhuse/web-intelligence-data/master/country_codes.json"
level2_divisions = "https://raw.githubusercontent.com/alecdhuse/web-intelligence-data/master/level-2-divisions.json"
ca_postal_codes = "https://raw.githubusercontent.com/alecdhuse/web-intelligence-data/master/ca_postal_codes.json"
nz_postal_codes = "https://raw.githubusercontent.com/alecdhuse/web-intelligence-data/master/nz_postal_codes.json"
us_postal_codes = "https://raw.githubusercontent.com/alecdhuse/web-intelligence-data/master/us_postal_codes.json"
source = "https://raw.githubusercontent.com/alecdhuse/web-intelligence-data/master/university_networks.json"
nominatim = Nominatim()

# Load country codes
cc_data = urllib2.urlopen(country_codes)
country_codes_json = json.load(cc_data)

# Load level 2 divisions
lvl2_data = urllib2.urlopen(level2_divisions)
level2_divisions_json = json.load(lvl2_data)

# Load postal codes
postal_code_json_ca = json.load(urllib2.urlopen(ca_postal_codes))
postal_code_json_nz = json.load(urllib2.urlopen(nz_postal_codes))
postal_code_json = json.load(urllib2.urlopen(us_postal_codes))

# Load source data
data = urllib2.urlopen(source)
json_data = json.load(data)

for entry in json_data['universities']:
    uni_name = entry['name']
    obj_data = Object_info()
    
    if not ('osm' in entry):
        result = nominatim.query(uni_name)
        
        if (len(result) == 1):
            obj_info     = parse_object_info(result[0]['display_name'])
            obj_info.lon = float(result[0]['lon'])
            obj_info.lat = float(result[0]['lat'])

            if len(obj_info.country) > 0: 
                for network in entry['networks']:
                    network['country']  = obj_info.country
                    network['city']     = obj_info.city
                    network['division'] = obj_info.lvl2_div
                    network['code']     = obj_info.post_code
                    network['lng']      = obj_info.lon
                    network['lat']      = obj_info.lat

                entry['osm'] = True
                print "Updated info for " + uni_name
                print "\t" + str(obj_info)
            else:
                print "Info Error"
                print result[0]['display_name']
                print obj_info
                print "----"
                
        elif (len(result) > 1):
            print "Multiple results for " + uni_name

            for r in result:
                fist_display_token = r['display_name'].split(',')[0]
                
                if fist_display_token == uni_name or fist_display_token == uni_name[:4]:
                    display_name = r['display_name'].split(',')
                    obj_info     = parse_object_info(result[0]['display_name'])
                    obj_info.lon = float(result[0]['lon'])
                    obj_info.lat = float(result[0]['lat'])

                    if len(obj_info.country) > 0: 
                        for network in entry['networks']:
                            network['country']  = obj_info.country
                            network['city']     = obj_info.city
                            network['division'] = obj_info.lvl2_div
                            network['code']     = obj_info.post_code
                            network['lng']      = obj_info.lon
                            network['lat']      = obj_info.lat

                        entry['osm'] = True
                        print "\tUpdated info for " + uni_name
                        print "\t\t" + str(obj_info)
                    else:
                        print "Info Error"
                        print result[0]['display_name']
                        print obj_info
                        print "----"
                
                    break
                else:
                    print "\tCould not resolve single entry for " + fist_display_token
                    entry['osm'] = False
        else:
            print "No results for " + uni_name
            entry['osm'] = True

        time.sleep(11)

        with open('data.txt', 'w') as outfile:
            json.dump(json_data, outfile)
