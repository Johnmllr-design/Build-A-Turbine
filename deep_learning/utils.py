# A file to hold auxillary utility methods for abstraction
import csv
import os
from typing import List




# get the power curve data into an array for storage
def get_power_curve_dataset():
    data = []
    # Open the file for reading ('r')
    with open("/Users/johnmiller/Desktop/buildaturbine/deep_learning/wind_turbine_library.csv", mode='r') as csvfile:

        # parse each row into a dictionary
        reader = csv.DictReader(csvfile)

        # append each given row to the ground truth list
        for row in reader:
            data.append(row)
    return data


 # remove non alphanumeric chars 
def get_string(input_string : str) -> str:
    ret = ""
    for char in input_string:
        if char.isalnum():
            ret += char
    return ret.lower()



# convert the array represented as a string to an array
def to_array(array_string: str):
    ret = []
    cur = ""
    print("we got the initial wind values " + array_string)
    for char in array_string:
        if char.isdigit():
            if int(char) > 0:
                    cur += char
        else:
            if cur != "":
                ret.append(int(cur))
                cur = ""
    return ret

# convert the array represented as a string to an array (for floats)
def to_array_float(array_string: str):
    ret = []
    cur = ""
    for char in array_string:
        if char.isdigit() or char == '.':
            cur += char
        else:
            if cur != "":
                ret.append(float(cur))
                cur = ""
    return ret


