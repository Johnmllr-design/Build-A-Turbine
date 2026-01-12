import torch
import numpy
import torch.nn as nn
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
                cur[1] = cur[2] # fix long/lat flipflop
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
        
        # normalize the data
        dataset = self.normalize_data(dataset)
        


        # sort the turbines for subsequent embedding
        turbines = list(set([arr[0] for arr in dataset]))
        turbines.sort()

        # declare a tensor of turbine embeddings
        turbine_tensor_embeddings = torch.rand(len(turbines), 3) 

        # save the embeddings, the turbine types, and the dataset
        torch.save(turbine_tensor_embeddings, f="type_embeddings.pt")
        numpy.save('dataset.npy', dataset)
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

    # perform min/max normalization
    def normalize_data(self, dataset):
        lat = [dat[1] for dat in dataset]
        long = [dat[2] for dat in dataset]
        pred = [dat[3] for dat in dataset]
        minLat = min(lat)
        minLong = min(long)
        minobs = min(pred)
        rangeLat = abs(max(lat) - min(lat))
        rangeLong = abs(max(long) - min(long))
        rangeObs = abs(max(pred) - min(pred))

        # normalize the dataset
        for observation in dataset:
            observation[1] = ((observation[1] - minLat) / rangeLat)
            observation[2] = ((observation[2] - minLong) / rangeLong)
            observation[3] = ((observation[3] - minobs) / rangeObs)
        return dataset



# driver code for a one-time cleaning and saving of the sataset to the directory
if __name__ == '__main__':
    clean_dataset().clean_data()
    dataset = numpy.load('dataset.npy')
    print("")
    print(dataset)
    print(torch.load('type_embeddings.pt'))


        