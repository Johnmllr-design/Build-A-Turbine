import torch
from torch.optim import Adam
import torch.nn as nn
from torch import Tensor

class TurbinePredictionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.sigmoid = nn.Sigmoid()
        self.relu = nn.ReLU()
        self.initial_layer = nn.Linear(in_features=5, out_features=30, bias=True)
        self.hidden_layer = nn.Linear(in_features=30, out_features=60, bias=True)
        self.hidden_layer_2 = nn.Linear(in_features=60, out_features=30, bias=True)
        self.hidden_layer_3 = nn.Linear(in_features=30, out_features=15, bias=True)
        self.output_layer = nn.Linear(in_features=15, out_features=1)




    def forward(self, input:Tensor):
        first_output = self.relu(self.initial_layer(input))
        second_output = self.relu(self.hidden_layer(first_output))
        third_output = self.relu(self.hidden_layer_2(second_output))
        fourth_output = self.relu(self.hidden_layer_3(third_output))
        prediction = self.output_layer(fourth_output)
        return prediction





