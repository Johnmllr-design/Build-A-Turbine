# A file to hold auxillary utility methods for abstraction
import csv
import os
from typing import List
import torch
import numpy




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


# get the user turbine options
def get_user_options():
    data = []
    # Open the file for reading ('r')
    with open("/Users/johnmiller/Desktop/buildaturbine/deep_learning/wind_turbine_library.csv", mode='r') as csvfile:

        # parse each row into a dictionary
        reader = csv.DictReader(csvfile)

        # append each given row to the ground truth list
        for row in reader:
            if row["has_power_curve"]:
                data.append([row["manufacturer"], row["name"]])
    with open("makes_and_models.txt", mode="w") as text_file:
        text_file.write(str(data))
        text_file.flush()
    
    



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


# Find the corresponding key for the wind power curve
def match_key_to_value(key: float, corresponding_values: List):
    if key > max(corresponding_values):
        return 0
    else:
        max_difference = 10000
        best_index = 0
        for i in range(0, len(corresponding_values)):
            if abs(corresponding_values[i] - key) < max_difference:
                max_difference = abs(corresponding_values[i] - key)
                best_index = i
        return best_index
    

def string_to_int(s):
    ret = ""
    for char in s:
        ret += str(ord(char))
        ret += "0"
    print(ret)
    return int(ret)

# find the corresponding turbine embedding
def find_embeddings(type, types):
    for i, possible in enumerate(types):
        if possible == type:
            return i
    return -1

# normalize and standardize a provided input to a tensor-ready option
def normalize_input(input:List):

    normalized_input = []

    normalization_values = numpy.load('min_max_normalization_values.npy')
    type_strings = numpy.load('turbine_types.npy')
    type_embeddings = torch.load('type_embeddings.pt')
    print(normalization_values)
    print(type_strings)
    print(type_embeddings)
    correct_embedding = type_embeddings[find_embeddings(input[0], type_strings)]
    for value in correct_embedding:
        normalized_input.append(value)
    normalized_input.append((input[1] - normalization_values[0] / normalization_values[1])) # normalize the latitude
    normalized_input.append((input[2] - normalization_values[2] / normalization_values[3])) # normalize the latitude
    print("normalized input is ", normalized_input)
    return normalized_input

# normalize and standardize a provided input to a tensor-ready option
def normalize_input_2(input:List):
    normalized_input = []
    type_strings = numpy.load('turbine_types.npy')
    type_embeddings = torch.load('type_embeddings.pt')
    correct_embedding = type_embeddings[find_embeddings(input[0], type_strings)]
    for value in correct_embedding:
        normalized_input.append(value)
    normalized_input.append(input[1])
    normalized_input.append(input[2])
    print("normalized input is ", normalized_input)
    return normalized_input


# normalize and standardize a provided input to a tensor-ready option
def de_normalize_output(output):
    normalization_values = numpy.load('min_max_normalization_values.npy')
    return output * normalization_values[5] + normalization_values[4]




