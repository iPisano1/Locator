"""
Team Name: ByteForce
Members:
- Carlos, Rendyl John
- Augusto, John Michael
- Arellano, Jean

Unique Feature:
- Displays Estimated Arrival Time based on current time and trip duration
- Added Feature 2: Input Validation Improvement for starting and destination locations
"""

import requests
import urllib.parse
from datetime import datetime, timedelta

route_url = "https://graphhopper.com/api/1/route?"
key = "cbd570ae-e324-40f2-9bb6-363c0202563b"

def geocoding(location, key):
    while location == "":
        location = input("Enter the location again: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")

        if state and country:
            new_loc = name + ", " + state + ", " + country
        elif country:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Geocode API status: " + str(json_status) + "\nError message: " + json_data["message"])

    return json_status, lat, lng, new_loc

    # Added Feature 2: Input Validation Improvement
def get_valid_location(prompt):
    while True:
        loc = input(prompt)
        if loc.lower() in ["quit", "q"]:
            return None  
        if not loc.replace(" ", "").isalpha():
            print("Invalid input. Please enter a valid location (letters only).")
        else:
            return loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehicle profiles available on Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")

    profile = ["car", "bike", "foot"]
    vehicle = input("Enter a vehicle profile from the list above: ")

    if vehicle.lower() in ["quit", "q"]:
        break
    elif vehicle not in profile:
        vehicle = "car"
        print("No valid vehicle profile was entered. Using the car profile.")

    # Use Input Validation Feature 
    loc1 = get_valid_location("Starting Location: ")
    if loc1 is None:
        break
    orig = geocoding(loc1, key)

    loc2 = get_valid_location("Destination: ")
    if loc2 is None:
        break
    dest = geocoding(loc2, key)

    print("=================================================")

    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])

        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp

        response = requests.get(paths_url)
        paths_status = response.status_code
        paths_data = response.json()

        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
        print("=================================================")
        print("Directions from " + orig[3] + " to " + dest[3] + " by " + vehicle)
        print("=================================================")

        if paths_status == 200:
            distance_m = paths_data["paths"][0]["distance"]
            time_ms = paths_data["paths"][0]["time"]

            miles = distance_m / 1000 / 1.61
            km = distance_m / 1000

            sec = int(time_ms / 1000 % 60)
            mins = int(time_ms / 1000 / 60 % 60)
            hr = int(time_ms / 1000 / 60 / 60)

            print("Distance Traveled: {0:.1f} miles / {1:.1f} km".format(miles, km))
            print("Trip Duration: {0:02d}:{1:02d}:{2:02d}".format(hr, mins, sec))

            now = datetime.now()
            travel_time = timedelta(hours=hr, minutes=mins, seconds=sec)

            # Added Feature 1: Estimated Arrival Time
            arrival_time = now + travel_time
            print("Estimated Arrival Time:", arrival_time.strftime("%H:%M:%S"))

            print("=================================================")

            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} miles )".format(path, distance / 1000, distance / 1000 / 1.61))

            print("=================================================")
        else:
            print("Error message: " + paths_data["message"])
            print("*************************************************")