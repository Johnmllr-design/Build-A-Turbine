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
from utils import get_power_curve_dataset, get_string, to_array, to_array_float
import csv

base_url = "https://energy.usgs.gov/api/uswtdb/v1/turbines?&offset=1&limit=1"


#TurbineDatasetCurator is the data-gathering module underpinning buildATurbine's efficacious logic
class TurbineDatasetCurator:

    # initialize the class with the dataset
    def __init__(self):
        self.power_curve_data = get_power_curve_dataset()
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

        
        
        
    # Calculate_average_power uses the power curve we found to make manufacturer-accurate and historically thorough 
    # data-based calculations of daily electricity production
    def calculate_average_power(self, longitude:str, latitude:str, start_date: str, end_date:str, wind_speeds: List, corresponding_power_outputs: List):

        # track the number of days the turbine has been producing energy, and the amount of energy produced
        # TODO: account for floats as wind speed keys for the power calculations
        days_productive = 0
        net_production = 0

        API_endpoint = self.base_url + latitude + "," + longitude + "/" + start_date + "/" + end_date +  "?key=X2VF5PX638PV2KE6F8BK37RX4&include=days&elements=datetime,windspeedmean"
        print("attempting to hit " + API_endpoint)
        response = requests.get(API_endpoint)

        if response.status_code == 200:
            json = response.json()
            daily_wind_values = json['days']

            for day in daily_wind_values:
                wind_speed = float(day['windspeedmean'])
                print("checking if " + str(wind_speed) + " is in " + str(wind_speeds))
                if wind_speed in wind_speeds:
                    net_production += corresponding_power_outputs[wind_speeds.index(wind_speed)]
                    days_productive += 1
            
            return (net_production / days_productive)
        
        else:
            print("unable to hit this endpoint")
            print(response.status_code)
            return None    

    # create_dataset provides the core functionality for creating the inputs + 
    # ground truth information for the pytorch model to learn from. It iterates throug
    # the turbine dataset, retrieving the necessary data from each turbine to 
    # quantify the turbines' value
    def get_dataset(self):
        done_processing = False
        dataset = []
        index = 1
        while not done_processing:

            # make an API call to the USGS
            new_datapoint = []  # holder of new data
            base_url = f"https://energy.usgs.gov/api/uswtdb/v1/turbines?&offset={index * 1005}&limit=1"
            response = requests.get(base_url)

            # If unable to get turbine information, end early
            if response.status_code != 200 or len(response.json()) == 0:
                print("HERE: Unable to get a new input turbine. the response was " + str(response.status_code))

            # otherwise, if able to get a new turbine from the query, get it's information
            else:
                turbine_info = response.json()[0]
                longitude = turbine_info['xlong']
                latitude = turbine_info['ylat']
                year_operational = turbine_info['p_year']
                turbine_model = turbine_info['t_model']
                turbine_manufacturer = turbine_info['t_manu']

                # Get the turbine power curve based on the 
                if turbine_model != None:
                    result = self.get_turbine_curve(turbine_model)
                    if result != None:
                        start_date = str(year_operational) + "-01-01"
                        end_date = "2025-12-12"
                        average_power = self.calculate_average_power(str(longitude), str(latitude), start_date, end_date, result[0], result[1])
                        # TODO: implement lifelong costs of this turbine to calculate the gorund truth lifetime-kWd/lifetime cose value
                        
                        

                    # go to next possible turbine
                    else:
                        print(turbine_model + " power curve not in dataset")
            
            index += 1      # go to next turbine
        
        
    

    # find the matching furve for the provided turbine
    def get_turbine_curve(self, turbine_model: str) -> List:
            # get the reduced string for ease of string comparison
            turbine_model_reduced_string = get_string(turbine_model)

            # Iterate through the power curves dataset to find a matching turbine's wind curve
            for row in self.power_curve_data:
                # get the row's string
                reduced_row_string = get_string(row['name'])
                if len(reduced_row_string) > 0:
                    if reduced_row_string in turbine_model_reduced_string or turbine_model_reduced_string in reduced_row_string:
                        if row['has_power_curve'] == "True":
                           return to_array_float(row['power_curve_wind_speeds']), to_array_float(row['power_curve_values'])
                        else:
                            return None
            
            # if no matching curve found, return none
            return None


    def get_lifetime_costs(self, model:str):
        # TODO: implement finding of the lifetime cost of the turbine 
        pass




dummy_result = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/London,UK/last30days?key=X2VF5PX638PV2KE6F8BK37RX4&include=days&unitGroup=metric&elements=datetime,windspeedmean"

# test = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Denver,CO?unitGroup=metric&key=YOUR_API_KEY&contentType=csv&include=days&elements=datetime,temp,windspeed50,winddir50,windspeed80,winddir80,windspeed100,winddir100"


obj = TurbineDatasetCurator()
obj.get_dataset()



