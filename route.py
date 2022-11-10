#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by:
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022
#


# !/usr/bin/env python3
import sys
import pandas as pd
import pandas as pd
import math
import numpy as np
from math import radians, cos, sin, asin, sqrt
import sys
from queue import PriorityQueue
import sys
from math import tanh
import heapq
import numpy as np

def get_data():
    data = pd.read_csv('city-gps.txt', sep = ' ', index_col = None, names=["City", "latitude", "Longitude"])
    lat_long = data.set_index('City').T.to_dict('list')
    data1 = pd.read_csv('road-segments.txt', sep = ' ', index_col = None, names = [ 'first_city', 'second_city', 'length', 'speed_limit', 'name_of_highway'])
    data2 = data1.copy()
    data2.rename(columns={"first_city": "second_city", "second_city": "first_city"},inplace = True )
    data_final = data1.append(data2)
    data_final.drop_duplicates(inplace=True)
    data_list = data_final.values.tolist()
    return lat_long, data_final

def haversine_dist(city1, city2,data):
    if city1 not in data.keys() or city2 not in data.keys():
        return 0
    city1 = data[city1]
    city2 = data[city2]
    # this function gives the haversine distance in miles between any two cities
    city1_long = radians(city1[1])
    city2_long = radians(city2[1])
    city1_lat = radians(city1[0])
    city2_lat = radians(city2[0])

    temp_distance = 2 * asin(sqrt(sin((city2_lat - city1_lat)/2) ** 2 + cos(city1_lat) * cos(city2_lat) * sin((city2_long - city1_long)/2) ** 2))

    return temp_distance*3956

def successors(data_list,city):
    succ = []
    for i in data_list:
        if i[0] == city:
            succ.append(i[1])
    return succ

def is_goal(state,city2):
    return state == city2


def solve(city1,city2, data_list,lat_long):
    fringe = PriorityQueue()
    count = 0
    fringe.put((count,(city1,[])))
    while ( not fringe.empty()):
        
        gg = (fringe.get())
        (state, path) = gg[1]
        
        
        if is_goal(state,city2):
            return path+[state,]
        
        count+=1
        for s in successors(data_list,state):
            fringe.put((len(path)+haversine_dist(s,city2,lat_long),(s, path+[state])))
            
    return []

def calc_heuristic(cost, path, total_miles, segments, total_hours, total_delivery_hours, gps, city2, road ,next_distance, max_segment , max_speed, next_speed, next_time):
    node_city = path[-1]
 
    if cost == "distance":
        desti_path = haversine_dist(node_city, gps, city2, road)     # we are finding the distance from the cordinates using Haversine distance
        d = desti_path + total_miles                            
        return d
    
    elif cost == 'time':
        desti_path = haversine_dist(node_city, gps, city2, road)     # Compute the distance between two cities                    
        t = float(desti_path/float(max_speed)) + total_hours   # The cost function for TIME- is the sum of (Haversine distance to the End City divided by the Maximum speed) to the total_hours. This way we keep the cost function admissable since any speed less than the max speed will give a greater time. We use the same function for delivery and calculate the total delivery time later in a seperate function.
        return t  

    elif cost == 'delivery':
        desti_path = haversine_dist(node_city, gps, city2, road)     # Compute the distance between two cities           
        t_heur = float(desti_path/float(max_speed))
        t_reroute = calc_delivery(next_time, next_distance, next_speed, total_delivery_hours)   # The cost functon is DELIVERY- it computes the given formula are returns the time.
        t_del = t_heur + t_reroute
        return t_del
    
    elif cost == "segments":
        s = float(next_distance/float(max_segment)) + segments       #The cost function for SEGMENTS- is the addition of (length of the particular road segment divided by the maximum segment length) to the total_segments travelled and estimated Haversine distance to the End city. This way we keep the cost function admissable since any segment length will not be greater than the maximum segment length.
        return s

def calc_delivery(next_time, next_distance, next_speed, total_delivery_hours):
    t_trip = total_delivery_hours - next_time
    l=next_distance
    speed=next_speed
    t_road = float(l/speed)
    t=0
    if speed >= 50.0:   # if speed>50 , calculate the extra rerouting distance  with the given probability function.
        prob = math.tanh(l/1000)
        t = t_trip+ t_road + prob*(2*(t_trip+t_road))  

    elif speed < 50.0:   # if speed<50, calculate the total distance without rerouting.
        t = t_road + t_trip

    return t

def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    lat_long, data_list = get_data()
    
    route_taken =[]
    return {"total-segments" : len(route_taken), 
            "total-miles" : 51., 
            "total-hours" : 1.07949, 
            "total-delivery-hours" : 1.1364, 
            "route-taken" : route_taken}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    lat_long, gps_data= get_data()
    print(gps_data.head())
    

    # if len(sys.argv) != 4:
    #     raise(Exception("Error: expected 3 arguments"))

    # (_, start_city, end_city, cost_function) = sys.argv
    # if cost_function not in ("segments", "distance", "time", "delivery"):
    #     raise(Exception("Error: invalid cost function"))

    # result = get_route(start_city, end_city, cost_function)

    # # Pretty print the route
    # print("Start in %s" % start_city)
    # for step in result["route-taken"]:
    #     print("   Then go to %s via %s" % step)

    # print("\n          Total segments: %4d" % result["total-segments"])
    # print("             Total miles: %8.3f" % result["total-miles"])
    # print("             Total hours: %8.3f" % result["total-hours"])
    # print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


