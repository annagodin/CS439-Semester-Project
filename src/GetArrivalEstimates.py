from datetime import datetime
import json
import time
import requests
import csv

# loop control variable, start at 1 hour = 3600 seconds
a = 3600

with open('../stop_data.json') as json_file:
    stop_data = json.load(json_file)
stop_data = stop_data['data']

with open('../route_data.json') as json_file:
    route_data = json.load(json_file)
route_data = route_data['data']['1323']


def get_weekday(weekday_int):
    switcher = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
    }
    return switcher.get(weekday_int, "Invalid input")


# gives stop coordinates given a stop ID
def get_stop_coordinates(stop_data, stop_id):
    for stop in stop_data:
        if stop['stop_id'] == stop_id:
            return stop['location']


# gives stop coordinates given a stop ID
def get_stop_name(stop_data, stop_id):
    for stop in stop_data:
        if stop['stop_id'] == stop_id:
            return stop['name']


# gives route full name given a route ID
def get_route_name(route_data, route_id):
    for route in route_data:
        if route['route_id'] == route_id:
            return route['long_name']


def write_result_data(vehicles):
    with open('bus_dataTESTING.csv', 'a+', newline='') as file:
        writer = csv.writer(file)
        # iterate through the buses that are on the specified route
        for bus in vehicles:
            # print(json.dumps(bus, indent=2))
            print('----------------------------------------------------------------------------------------')

            arrival_estimates = bus['arrival_estimates']
            for eta in arrival_estimates:
                arrival_at_string = eta['arrival_at']
                arrival_at_string= arrival_at_string[:-6]
                # print(arrival_at_string)
                # exit(1)
                arrival_datetime = datetime.strptime(arrival_at_string, '%Y-%m-%dT%H:%M:%S')
                arrival_datetime = arrival_datetime.replace(tzinfo=None)
                minutes_to_arrival = (arrival_datetime - current_datetime).seconds
                minutes_to_arrival = round(minutes_to_arrival / 60)

                bus_id = bus['vehicle_id']
                bus_long = bus['location']['lng']
                bus_lat = bus['location']['lat']

                route_id = eta['route_id']
                route_name = get_route_name(route_data, route_id)

                stop_id = eta['stop_id']
                stop_coordinates = get_stop_coordinates(stop_data, stop_id)
                stop_name = get_stop_name(stop_data, stop_id)
                stop_long = stop_coordinates['lng']
                stop_lat = stop_coordinates['lat']
                weekday = get_weekday(current_datetime.weekday())

                # print("Arrival DateTime: " + str(arrival_datetime))
                # print("Current DateTime: " + str(current_datetime))
                # print("Day of Week: " + weekday)
                # print("Minutes to Arrival: " + str(minutes_to_arrival))
                # print("Route ID: " + route_id)
                # print("Route Name: " + route_name)
                # print("Bus ID: " + bus_id)
                # print("Bus Lat: " + str(bus_lat))
                # print("Bus Long: " + str(bus_long))
                # print("Stop ID: " + stop_id)
                # print("Stop Name: " + stop_name)
                # print("Stop Lat: " + str(stop_lat))
                # print("Stop Long: " + str(stop_long))
                row = [str(arrival_datetime), str(current_datetime), weekday, str(minutes_to_arrival), route_id, route_name,
                       bus_id, str(bus_lat), str(bus_long), stop_id, stop_name, str(stop_lat), str(stop_long)]
                print(row)
                writer.writerow(row)


# --------------------------------------------------------------------------------------------------------#

url = "https://transloc-api-1-2.p.rapidapi.com/vehicles.json"

# LX Route
# querystring = {"routes": "4012630", "callback": "call", "agencies": "1323"}

querystring = {"callback": "call", "agencies": "1323"}

headers = {
    'x-rapidapi-host': "transloc-api-1-2.p.rapidapi.com",
    'x-rapidapi-key': "2dfca44683mshac07ff2b9052a02p112b96jsn531257731503"
}

while a > 0:
    response = requests.request("GET", url, headers=headers, params=querystring)
    current_datetime = datetime.now()
    response_json = json.loads(response.text)
    # get vehicles that are on the specified route
    vehicles = response_json['data']['1323']
    write_result_data(vehicles)
    time.sleep(10)
    a -= 10
