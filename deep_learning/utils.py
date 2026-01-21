# A file to hold auxillary utility methods for abstraction
import csv
import os
from typing import List
import torch
import numpy





# normalize turbine model names
def normalize_model_string(string):
    ret = ""
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    contains_char = False
    for char in string:
        if char.isalpha():
            ret = ret + char.lower()
            contains_char = True
        elif char in numbers:
            ret = ret + char
    if contains_char:
        return ret


def get_speed(daily_speed):
    speeds = [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16,16.5,17,17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27,27.5,28,28.5,29,29.5,30,30.5,31,31.5,32,32.5,33,33.5,34,34.5,35]
    diff = 10000
    ret = -1
    for speed in speeds:
        if abs(float(daily_speed) - speed) < diff:
            diff = abs(float(daily_speed) - speed)
            ret = speed
    return str(ret)