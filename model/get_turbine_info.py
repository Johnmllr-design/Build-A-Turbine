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

    # create_dataset provides the core functionality for creating the inputs + 
    # ground truth information for the pytorch model to learn from. It iterates throug
    # the turbine dataset, retrieving the necessary data from each turbine to 
    # quantify the turbines' value
    def create_dataset(self):
        
        done_processing = False
        index = 0
        dataset = []
        while not done_processing:

            new_datapoint = []  # holder of new data
            base_url = f"https://energy.usgs.gov/api/uswtdb/v1/turbines?&offset={index}&limit=1"
            response = requests.get(base_url)
            if response.status_code != 200:
                done_processing = True
                print("processign terminated")
            else:
                # get the necessary turbine information
                turbine_info = response.json()[0]
                longitude = turbine_info['xlong']
                latitude = turbine_info['ylat']
                year_operational = turbine_info['p_year']
                turbine_model = turbine_info['t_model']
                turbine_manufacturer = turbine_info['t_manu']

                # Get the turbine power curve based on the 
                wind_speeds, power_outputs = self.get_turbine_curve(turbine_model, turbine_manufacturer)

                # use the power curve for the given model to calculate the average power output of the turbine per day
                start_data = year_operational + "01/01/" + year_operational
                current_date = "06/06/2025"
                lifetime_average_daily_power = self.calculate_average_power()

                # use the finance method to determine the cost of setting up and maintaining this turbine over time
                lifetime_operational_cost = self.get_lifetime_costs(turbine_model)

                # ground truth value, represented as daily kiloWattage over dollar
                kW_per_dollar = lifetime_average_daily_power / lifetime_operational_cost

                new_data = [[longitude, latitude, turbine_model], [kW_per_dollar]]
                dataset.append(new_data)
        
        # TO DO: convert array to numpy array and save for training
        numpy_dataset = np.array(new_data)
        



                    
                        

            
            
            
            # this will provide with the weather data at the turbines location for the duration of its operation
            # location_api_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" + str(latitude) + "," + str(longitude) + "/" + str(year_operational) + "-01-01/2025-01-01?key=X2VF5PX638PV2KE6F8BK37RX4"
            # print(location_api_url)
            # result = requests.get(location_api_url)

    
    def get_turbine_curve(self, turbine_make, turbine_model) -> List:
        # TODO: implement with the WindPower API to get the given turbines curve
        pass

    def calculate_average_power(self, start_dat: str, end_date:str, wind_speeds: List, corresponding_power_outputs: List):
        # TODO: implement with the VisualCrossing API to get the given turbines curve
        pass

    def get_lifetime_costs(self, model:str):
        # TODO: implement finding of the lifetime cost of the turbine 
        pass


    def get_string(self, input_string : str) -> str:
        ret = ""
        for char in input_string:
            if char.isalnum():
                ret += char
        return ret.lower()
    






o = TurbineDatasetCurator()
o.get_turbine_info()