# get_turbine_info.py is a module that works in compliment to the
# backend CRUD/database operations of the jaa application, and provides 
# backend logic for retrieving and learning the relationships between 
# the following key input :

# 1: turbine average kiloWattage over time, found by calculating the 
# (maximum rated capacity in kW, P * CF, Capacity factor * hourss per year)
# where we can get capacity factor as follows CF = 0.087vavg​−0.125


import os
import json
from typing import List
from random import random
import requests
import numpy as np
import csv

base_url = "https://energy.usgs.gov/api/uswtdb/v1/turbines?&offset=1&limit=1"


#TurbineDatasetCurator is the data-gathering module underpinning buildATurbine's efficacious logic
class TurbineDatasetCurator:

    # initialize the class with the dataset
    def __init__(self):
        self.power_curve_data = self.get_power_curve_dataset()
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
   

    
    def get_turbine_curve(self, turbine_model: str) -> List:
        # get the reduced string for ease of string comparison
        turbine_model_reduced_string = self.get_string(turbine_model)

        # Iterate through the power curves dataset to find a matching turbine's wind curve
        for row in self.power_curve_data:
            # get the row's string
            reduced_row_string = self.get_string(row['name'])
            if len(reduced_row_string) > 0:
                if reduced_row_string in turbine_model_reduced_string or turbine_model_reduced_string in reduced_row_string:
                    print(turbine_model +"  is in the dataset and matches with " + str(reduced_row_string) + " of length " + str(len(reduced_row_string)))
                    if row['has_power_curve']:
                        return row['power_curve_wind_speeds'], row['power_curve_values']
        
        # if no matching curve found, return none
        return None



            

    # get the power curve data into an array for storage
    def get_power_curve_dataset(self):
        data = []
        # Open the file for reading ('r')
        with open("/Users/johnmiller/Desktop/buildaturbine/deep_learning/wind_turbine_library.csv", mode='r') as csvfile:

            # parse each row into a dictionary
            reader = csv.DictReader(csvfile)

            # append each given row to the ground truth list
            for row in reader:
                data.append(row)
        return data

        
        
        
    # Calculate_average_power uses the power curve we found to make manufacturer-accurate and historically thorough 
    # data-based calculations of daily electricity production
    def calculate_average_power(self, longitude:str, latitude:str, start_date: str, end_date:str, wind_speeds: List, corresponding_power_outputs: List):
        # track the number of days the turbine has been producing energy, and the amount of energy produced
        days_productive = 0
        net_production = 0

        # get the API wind data for the current turbine
        API_endpoint = self.base_url + latitude + "," + longitude + "/" + start_date + "/" + end_date +  "?key=X2VF5PX638PV2KE6F8BK37RX4&include=days&elements=datetime,windspeedmean"
        print(API_endpoint)
        result = requests.get(API_endpoint)
        json_results = result.json()
        daily_wind_values = json_results['days']

        # use the power curve in conjunction with the turbines data to get the turbines output for each day
        for day in daily_wind_values:
            wind_speed = int(day['windspeedmean'])
            if wind_speed in wind_speeds:

                print(wind_speed +" is a valid wind speed in the curve")
                # increment net production and increment number of observations
                net_production += corresponding_power_outputs[wind_speeds.index(wind_speed)]
                days_productive += 1
        
        return (net_production / days_productive)



    def get_lifetime_costs(self, model:str):
        # TODO: implement finding of the lifetime cost of the turbine 
        pass


    # remove non alphanumeric chars 
    def get_string(self, input_string : str) -> str:
        ret = ""
        for char in input_string:
            if char.isalnum():
                ret += char
        return ret.lower()
    

    # create_dataset provides the core functionality for creating the inputs + 
    # ground truth information for the pytorch model to learn from. It iterates throug
    # the turbine dataset, retrieving the necessary data from each turbine to 
    # quantify the turbines' value
    def get_dataset(self):
        done_processing = False
        dataset = []
        index = 0
        while not done_processing:

            # make an API call to the USGS
            new_datapoint = []  # holder of new data
            base_url = f"https://energy.usgs.gov/api/uswtdb/v1/turbines?&offset={index}&limit=1"
            response = requests.get(base_url)

            # If able to get a new turbine from the query, get it's information
            if response.status_code != 200:
                done_processing = True
                print("processign terminated")
            else:
                turbine_info = response.json()[0]
                longitude = turbine_info['xlong']
                latitude = turbine_info['ylat']
                year_operational = turbine_info['p_year']
                turbine_model = turbine_info['t_model']
                turbine_manufacturer = turbine_info['t_manu']

                # Get the turbine power curve based on the 
                wind_speeds, power_outputs = self.get_turbine_curve(turbine_model, turbine_manufacturer)

                # use the power curve for the given model to calculate the average power output of the turbine per day
                start_date = year_operational + "01/01/" + year_operational     # TODO: fix this
                current_date = "06/06/2025"                                     # TODO: fix this
                lifetime_average_daily_power = self.calculate_average_power(longitude, latitude, start_date, current_date)

                # use the finance method to determine the cost of setting up and maintaining this turbine over time
                lifetime_operational_cost = self.get_lifetime_costs(turbine_model)

                # ground truth value, represented as daily kiloWattage over dollar
                kW_per_dollar = lifetime_average_daily_power / lifetime_operational_cost

                new_data = [[longitude, latitude, turbine_model], [kW_per_dollar]]
                dataset.append(new_data)
        
        return dataset




dummy_result = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/London,UK/last30days?key=X2VF5PX638PV2KE6F8BK37RX4&include=days&unitGroup=metric&elements=datetime,windspeedmean"

# test = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Denver,CO?unitGroup=metric&key=YOUR_API_KEY&contentType=csv&include=days&elements=datetime,temp,windspeed50,winddir50,windspeed80,winddir80,windspeed100,winddir100"
# I need an upgraded plan for this one


result = requests.get(dummy_result)
print(result)
jsonn = result.json()
daily_data = jsonn['days']
for day in daily_data:
    print(day)
print(jsonn['queryCost'])
