from sys import argv
from typing import Tuple, Optional
import requests
import urllib.parse

# Assign values for further comparison
supply_level_mapping = {
    'low': 1, 
    'moderate': 2, 
    'optimal': 3, 
    'full': 4,
    'stop': 5,
}

# Use the Nominatim API to get the latitude and longitude of the donation centres
def get_coordinates(address: str, city: str, postal_code: str) -> Tuple[Optional[str], Optional[str]]:
    address = address.replace("ul. ","").replace("al. ","").replace("Ks. ","").replace("J. ","")
    location = f"{address}, {postal_code} {city}, Poland"
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote_plus(location)}&format=json"
    response = requests.get(url)
    data_donation_centers = response.json()
    if len(data_donation_centers) == 0: #is it empty?
        return None, None
    donation_center_latitude = data_donation_centers[0]['lat']
    donation_center_longitude = data_donation_centers[0]['lon']

    return donation_center_latitude, donation_center_longitude


def find_closest_donation_center(hospital_address: str, blood_type: str):
    nominatim_url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote_plus(hospital_address)}&format=json"
    response = requests.get(nominatim_url)
    data_hospital_address = response.json()
    hospital_latitude = data_hospital_address[0]['lat']
    hospital_longitude = data_hospital_address[0]['lon']

    
    # Use the blood level API to get the blood banks and their blood levels
    blood_level_url = "https://pl-blood-supply-api.vercel.app/blood-supply"
    response = requests.get(blood_level_url)
    inventory_data_of_donation_centres = response.json()

    
    closest_donation_center = None
    closest_distance = float("inf")
    
    # Iterate over the blood banks and find the one with the highest level of the specified blood type
    # that is closest to the hospital
    for donation_center in inventory_data_of_donation_centres:
        entry_blood_type = donation_center['bloodGroup']['groupString']
        if entry_blood_type != blood_type:
            continue
        
        address = donation_center['donationCenter']['streetAddress']
        postal_code = donation_center['donationCenter']['postalCode']
        city = donation_center['donationCenter']['city']
        donation_center_latitude, donation_center_longitude = get_coordinates(address, city, postal_code)
        if donation_center_latitude == None and donation_center_longitude == None:
            continue
        blood_donation_center_level = donation_center['supplyLevel']
     
        # Calculate the distance from the hospital to the blood bank
        distance = ((float(hospital_latitude) - float(donation_center_latitude)) ** 2 +
                  (float(hospital_longitude) - float(donation_center_longitude)) ** 2) ** 0.5 #in nautical miles
        blood_supply_level_value = supply_level_mapping[blood_donation_center_level]      # Check if the blood bank is closer than the current closest blood bank
        print(distance, city, blood_supply_level_value)
        
        # and if it has a higher level of the specified blood type
        if distance < closest_distance and blood_supply_level_value > supply_level_mapping["moderate"]:
            closest_distance = distance
            closest_donation_center = donation_center
    
    return closest_donation_center

if __name__=="__main__":

    hospital_address = argv[1]
    blood_type = argv[2]

    closest_donation_center = find_closest_donation_center(hospital_address, blood_type)

    print(closest_donation_center)
