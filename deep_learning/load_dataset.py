import torch
import numpy
import pandas as pd
import torch.nn as nn
import openpyxl
import csv
import re

class clean_dataset():
    def clean_data(self):
        # parse the values of the turbines and their latitudes
        strings = self.get_dataset_strings()
        cur = []
        dataset = []
        index = 0
        for i, value in enumerate(strings):
            if index == 5:
                cp = cur[1]
                cur[1] = cur[2] # fix long/lat flipflop so that is it lat/long
                cur[2] = cp
                dataset.append(cur)
                cur = []
                index = 0
            if index == 0:
                cur.append(value)
            elif index == 1:
                cur[0] += value
            elif index == 2 or index == 3 or index == 4:
                cur.append(float(value))
            index += 1
        


        # sort the turbines for subsequent embedding
        turbines = list(set([arr[0] for arr in dataset]))
        turbines.sort()

        # declare a tensor of turbine embeddings
        turbine_tensor_embeddings = torch.rand(len(turbines), 3) 

        # save the embeddings, the turbine types, and the dataset
        torch.save(turbine_tensor_embeddings, f="type_embeddings_rawdata.pt")
        numpy.save('dataset_rawdata.npy', dataset)
        numpy.save('turbine_types.npy', turbines)
    

    # get the strings of the entire dataset as a large blob
    def get_dataset_strings(self):
        strings = []
        with open('dataset.txt', 'r') as f:
            file_content = f.read()
            bad = [',', ']', '[', ' ', '\'' ]
            s = ""
            for char in file_content:
                if char not in bad:
                    s = s + char
                elif s != "":
                    strings.append(s)
                    s = ""
        f.close()
        return strings





# driver code for a one-time cleaning and saving of the sataset to the directory

if __name__ == '__main__':
    # Open the file for reading ('r')
    data = []
    with open("Power_curves.csv", mode='r') as csvfile:

        # parse each row into a dictionary
        data = csv.DictReader(csvfile)

        # append each given row to the ground truth list
        for row in data:
            print(str(row['Manufucturer Name']) + " " + str(row['Turbine Name']))

        