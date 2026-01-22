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
import pandas as pd
import random
import csv
import signal
from utils import normalize_model_string, get_speed


class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Function timed out")

signal.signal(signal.SIGALRM, timeout_handler)



# TurbineDatasetCurator is the data-gathering module underpinning buildATurbine's efficacious logic
class TurbineDatasetCurator:

    # initialize the class with the dataset
    def __init__(self):
        self.base_weather_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        self.base_turbine_url = "https://energy.usgs.gov/api/uswtdb/v1/turbines?&"
        self.known_turbines = []
        with open("Power_curves.csv", mode='r') as csvfile:

            # parse each row into a dictionary
            data = csv.DictReader(csvfile)

            # append each given row to the ground truth list
            for row in data:
                self.known_turbines.append(row)

        
        self.models = []
        for row in  self.known_turbines:
            if normalize_model_string(row['Turbine Name']) != None:
                self.models.append(normalize_model_string(row['Turbine Name']))


        
        
    # Calculate_average_power uses the power curve we found to make manufacturer-accurate and historically thorough 
    # data-based calculations of daily electricity production
    # track the number of days the turbine has been producing energy, and the amount of energy produced.
    # make an API call to see what the weather has been like for the lifetime of the current turbine
    def calculate_power(self, longitude:str, latitude:str, start_date: str, end_date:str, turbine_specifics:dict):
        print([longitude, latitude, start_date, end_date])
        days_productive = 0
        electricity_production = 0
        API_endpoint = self.base_weather_url + latitude + "," + longitude + "/" + start_date + "/" + end_date +  "?key=X2VF5PX638PV2KE6F8BK37RX4&include=days&elements=datetime,windspeedmean"
        response = requests.get(API_endpoint)
        print(response.status_code)
        

        # if a succesful call, make calculation
        if response.status_code == 200:
            json = response.json()
            daily_wind_values = json['days']

            for i, day in enumerate(daily_wind_values):
                try: 
                    wind_speed = day['windspeedmean']
                    if wind_speed != None:
                        electricity_production += float(turbine_specifics[get_speed(wind_speed)])
                        days_productive += 1
                except:
                    print("unable to access the wind speed for some reason after " + str(days_productive) + " accesses")
                        
            # return the average kWd-production over the lifetime of the turbine ()
            return (electricity_production / days_productive)
        
        else:
            print("unable to access this turbines wind history from the weather API")
            return None
            
     

    # create_dataset provides the core functionality for creating the inputs +  ground truth information for the pytorch model
    # to learn from. It iterates throug the turbine dataset, retrieving the necessary data from each turbine to 
    # quantify the turbines' value
    def get_dataset(self, i):
        dataset = np.load('dataset.npy', allow_pickle=True).tolist()
        try:
            done_processing = False
            index = i
            processed = 0
            while not done_processing:
                print(index)
                # make an API call to the USGS
                response = requests.get(self.base_turbine_url + "offset=" + str(index) + "&limit=1")
                new_turbine_observation = response.json()[0]
                index += 1
                found = False

                # find its corresponding dataset turbine
                for turbine in self.known_turbines:
                    if new_turbine_observation['t_model'] == turbine['Turbine Name']:
                        try:
                            found = True
                            signal.alarm(45)  # ⏱ timeout in seconds
                            average_kW_production = self.calculate_power(
                                str(new_turbine_observation['xlong']), 
                                str(new_turbine_observation['ylat']), 
                                str(new_turbine_observation['p_year']) + "-01-01",
                                "2025-12-12", 
                                turbine)


                            kW_per_dollar = average_kW_production / (float(new_turbine_observation['t_cap']) * 1000)   # use the factor of 1000 * rated capacity as 
                                                                                                                       # a ground truth of turbine price to get a proportion of kW-per-dollar
                            
                            # print it's final dataset observatio
                            print("the new observation is " + str([new_turbine_observation['t_model'], new_turbine_observation['ylat'], new_turbine_observation['xlong'], kW_per_dollar]))                     
                            dataset.append([new_turbine_observation['t_model'],  new_turbine_observation['xlong'], new_turbine_observation['ylat'], kW_per_dollar])
                            print("APPENDED A NEW OBSERVATION")

                            processed += 1
                        except TimeoutException:
                            print("❌ calculate_average_power took too long")
                        finally:
                            signal.alarm(0)  # cancel the alarm
                        break


            
                if processed >= 1 and found:
                    np.save('dataset.npy', np.array(dataset, dtype=object))
                    print("dataset has length " + str(len(dataset)))
        except:
            print("there was an exception")
            self.get_dataset(index)
                    
        
    



if __name__ == '__main__':
    obj = TurbineDatasetCurator()
    obj.get_dataset(5494)







