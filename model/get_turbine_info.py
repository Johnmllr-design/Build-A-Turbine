# get_turbine_info.py is a module that works in compliment to the
# backend CRUD/database operations of the jaa application, and provides 
# backend logic for retrieving and learning the relationships between 
# the following key input :

# 1: turbine average kiloWattage over time, found by calculating the 
# (maximum rated capacity in kW, P * CF, Capacity factor * hourss per year)
# where we can get capacity factor as follows CF = 0.087vavg​−0.125


import os
import json
import requests

base_url = "https://energy.usgs.gov/api/uswtdb/v1/turbines?&offset=1&limit=1"


def get_turbine_info():
    seen_turbine_models = []
    for i in range(0, 50000):

        # make this print to the same line
        print(f"at percentage {i / 50000}", flush=True, end="")
        base_url = f"https://energy.usgs.gov/api/uswtdb/v1/turbines?&offset={i}&limit=1"
        get_request = requests.get(base_url)
        if get_request.status_code == 200:
            turbine_json = get_request.json()[0]
            seen_turbine_models.append(turbine_json['t_model'])
            print()
            print(f"at percentage {i / 50000}, New Turbine Model Found: {turbine_json['t_model']}")
            print()
    
    print("there are " + str(len(seen_turbine_models)) + " unique turbine models")

    with open("turbine_models.txt", "w") as f:
        f.write(str(seen_turbine_models))

get_turbine_info()

