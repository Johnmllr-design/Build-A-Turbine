import torch
from torch.optim import Adam
import torch.nn as nn
from torch import Tensor

class TurbinePredictionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.sigmoid = nn.Sigmoid()
        self.initial_layer = nn.Linear(in_features=6, out_features=30, bias=True)
        self.hidden_layer = nn.Linear(in_features=30, out_features=15, bias=True)
        self.output_layer = nn.Linear(in_features=15, out_features=1)




    def forward(self, input:Tensor):
        first_output = self.sigmoid(self.initial_layer(input))
        second_output = self.sigmoid(self.hidden_layer(first_output))
        prediction = self.sigmoid(self.output_layer(second_output))
        return prediction





