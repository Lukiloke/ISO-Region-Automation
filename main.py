import csv
import pgeocode
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError
import sys

def try_pgeocode(country_code, postal_code, pgeocode_cache, current_line):

    print(" Attempting with pgeocode...")
    
    if country_code not in pgeocode_cache:
        try:
            pgeocode_cache[country_code] = pgeocode.Nominatim(country_code)
        except ValueError: 
            pgeocode_cache[country_code] = None
    
    nomi = pgeocode_cache[country_code]
    
    if nomi:
        resultat = nomi.query_postal_code(postal_code)
        iso_code_short = getattr(resultat, 'state_code', 'nan')
        iso_code_short = str(iso_code_short)

        if iso_code_short == 'nan' or not iso_code_short:
            current_line.append("No Data")
            print("✖️ No data in pgeocode")
        else:
            iso_code = f"{country_code}-{iso_code_short}"
            current_line.append(iso_code)
            current_line.append("pgeocode")
            print(f" Found (pgeocode) : {iso_code}")
    else:
        current_line.append("No Data (usc)")
        print(f"!!! Country not supported by pgeocode : {country_code}")


file_path =  input('Path to Source File: ')
export_path = input('Path to Output File: ')
start_index = 0
lines_to_process = 3762

try:
    with open(file_path, newline='', encoding='utf-8') as f:
        content_lists = list(csv.reader(f, delimiter=';'))
    print(f"File Read : {len(content_lists)} lines")
except FileNotFoundError:
    print(f"Error : File'{file_path}' doesn't exist.")
    exit()
except Exception as e:
    print(f"Error during the file read : {e}")
    exit()

end_line_index = min(start_index + lines_to_process, len(content_lists))

print("Initializing Nominatim...")
geolocator = Nominatim(user_agent="lukiloke_csv_filler") 
pgeocode_cache = {}

for i in range(start_index, end_line_index):
    current_line = content_lists[i]

    try:
        if len(current_line) >= 2:
            country_code = current_line[0].strip().upper()
            postal_code = str("0" + current_line[1].strip())
            if country_code == 'US' and len(postal_code) > 5:
                postal_code = postal_code[:5] 
            iso_code = None 

            print(f"\nLine {i}: Searching in Nominatim for: {postal_code}, {country_code}")

            query = {'postalcode': postal_code, 'country': country_code}
            location = geolocator.geocode(query,
                                          addressdetails=True,
                                          timeout=10)

            if location and location.raw:
                address_details = location.raw.get('address', {})
                iso_code_lvl6 = address_details.get('ISO3166-2-lvl6')
                iso_code_lvl4 = address_details.get('ISO3166-2-lvl4')

                if iso_code_lvl6:
                    iso_code = iso_code_lvl6
                    current_line.append(iso_code)
                    print(f" Found (lvl6) : {iso_code}")
                
                elif iso_code_lvl4:
                    iso_code = iso_code_lvl4
                    current_line.append(iso_code)
                    current_line.append("lvl4")
                    print(f" Found (lvl4) : {iso_code}")

                else:
                    print("No ISO data returned by Nominatim, falling back to pgeocode...")
                    try_pgeocode(country_code, postal_code, pgeocode_cache, current_line)
            
            else:
                print("X - Postal Code Not Found by Nominatim, falling back to pgeocode...")
                try_pgeocode(country_code, postal_code, pgeocode_cache, current_line) 
        else:
            print(f"Line {i}: Less than two colons, skipped")

        print("...requests cooldown...")
        time.sleep(1.1)

    except (GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError) as e:
        print(f"!!! Geopy service Error on line {i}: {e}", file=sys.stderr)
        current_line.append(f'Error: {e}')
    except Exception as e:
        print(f"Unexpected Error on line {i}: {e}", file=sys.stderr)
        current_line.append('Error: Unexpected')


try:
    with open(export_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(content_lists)
    print("\n\n---------------- CSV file updated with succes! -------------")
except Exception as e:
    print(f"\n Error during file write : {e}")


input('')
