import torch
import numpy


dataset = torch.load("dataset.pt")
print(dataset.__class__)
for tensor in dataset:
    print(tensor)