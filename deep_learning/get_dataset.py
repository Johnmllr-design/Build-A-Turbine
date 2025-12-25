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
import torch
import requests
import numpy as np
from utils import get_power_curve_dataset, get_string, to_array_float, match_key_to_value, string_to_int
import csv



#TurbineDatasetCurator is the data-gathering module underpinning buildATurbine's efficacious logic
class TurbineDatasetCurator:

    # initialize the class with the dataset
    def __init__(self):
        self.power_curve_data = get_power_curve_dataset()
        self.base_weather_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        self.base_turbine_url = "https://energy.usgs.gov/api/uswtdb/v1/turbines?&"


        
        
    # Calculate_average_power uses the power curve we found to make manufacturer-accurate and historically thorough 
    # data-based calculations of daily electricity production
    # track the number of days the turbine has been producing energy, and the amount of energy produced.
    # make an API call to see what the weather has been like for the lifetime of the current turbine
    # ! Preconditions: longitude and latitude must be decimal strings
    def calculate_average_power(self, longitude:str, latitude:str, start_date: str, end_date:str, wind_speeds: List, corresponding_power_outputs: List):

        days_productive = 0
        net_electricity_production = 0
        API_endpoint = self.base_weather_url + latitude + "," + longitude + "/" + start_date + "/" + end_date +  "?key=X2VF5PX638PV2KE6F8BK37RX4&include=days&elements=datetime,windspeedmean"
        response = requests.get(API_endpoint)


        if response.status_code == 200:
            json = response.json()
            daily_wind_values = json['days']

            for day in daily_wind_values:
                wind_speed = float(day['windspeedmean'])
                best_key_index = match_key_to_value(wind_speed, wind_speeds)
                net_electricity_production += corresponding_power_outputs[best_key_index]
                days_productive += 1
                        
            # return the average kWd-production over the lifetime of the turbine ()
            return (net_electricity_production / days_productive)
        
        else:
            print("unable to access this turbines wind history")
            return None
            
     

    # create_dataset provides the core functionality for creating the inputs +  ground truth information for the pytorch model
    # to learn from. It iterates throug the turbine dataset, retrieving the necessary data from each turbine to 
    # quantify the turbines' value
    def get_dataset(self):
        done_processing = False
        dataset = []
        index = 1500
        processed = 0
        while not done_processing:
            print("index " + str(index))

            # make an API call to the USGS
            new_datapoint = []  # holder of new data
            response = requests.get(self.base_turbine_url + "offset=" + str(index) + "&limit=1")
            index += 1      


            # If unable to get turbine information, skip turbine and continue
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
                turbine_rated_power_in_kW = turbine_info['t_cap']

                # Get the turbine power curve based on the 
                if turbine_model != None:
                    result = self.get_turbine_curve(turbine_model)
                    if result == None:
                        continue
                    else:
                        start_date = str(year_operational) + "-01-01"
                        end_date = "2025-12-12"
                        average_power = (self.calculate_average_power(str(longitude), str(latitude), start_date, end_date, result[0], result[1]) * 24) # convert to kWhours
                        costs = self.get_costs(float(turbine_rated_power_in_kW))

                        print()
                        print("this turbine " + turbine_manufacturer+ " " + turbine_model + " produced an average power of " + str(average_power) + "kilowatt hours per day during it's lifetime")
                        print("this turbine has costed " + str(costs))
                        print("# GROUND TRUTH: dollars for the average kWhours = " + str(costs / average_power))
                        print("on to the next turbine\n")
                        print()


                        # GROUND TRUTH: dollars for each average mWhours per day
                        ground_truth_dollar_per_kWh = costs / average_power

                        # append the observation
                        dataset.append([1, longitude, latitude, ground_truth_dollar_per_kWh])
                        processed += 1

                
            # check if we've gotten sufficient data observations. if so break the loop and save the dataset to a .pt file
            if index == 10000 or processed == 2:
                done_processing = True


        # save the tensors of data
        dataset_as_tensor = torch.tensor(dataset, dtype=torch.float32)
        torch.save(dataset_as_tensor, f = "dataset.pt")
    
        
    

    # find the matching furve for the provided turbine
    def get_turbine_curve(self, turbine_model: str) -> List:
            
            # get the reduced string for ease of string comparison
            turbine_model_reduced_string = get_string(turbine_model)

            # Iterate through the power curves dataset to find a matching turbine's wind curve
            # if no matching curve found, return none
            for row in self.power_curve_data:
                reduced_row_string = get_string(row['name'])
                if len(reduced_row_string) > 0:
                    if reduced_row_string in turbine_model_reduced_string or turbine_model_reduced_string in reduced_row_string:
                        if row['has_power_curve'] == "True":
                           return to_array_float(row['power_curve_wind_speeds']), to_array_float(row['power_curve_values'])
                        else:
                            return None
            return None


    # return the industry standard $100/kW of rated power times the actual rated power to 
    # obtain a coarse understanding of the cost to build the given turbine
    def get_costs(self, rated_power : float):
        print("finding the cost by multiplying 1000$ per rated kilowatt times the rating of " + str(rated_power) + " kilowatts")
        return (1000 * rated_power)
        
        






obj = TurbineDatasetCurator()
obj.get_dataset()
