from model import TurbinePredictionModel
import numpy
import torch
from utils import find_embeddings

class train_model():

    def __init__(self, learning_rate):
        self.model = TurbinePredictionModel()
        self.dataset = numpy.load('dataset.npy')       # numpy dataset array
        self.embeddings_Tensor = torch.load('type_embeddings.pt')
        self.turbine_types = numpy.load('turbine_types.npy')
        self.optim = torch.optim.Adam(params=self.model.parameters(), lr=learning_rate)
        self.loss = torch.nn.BCELoss()
        print(self.turbine_types)
        print(self.embeddings_Tensor)


    def train(self, epochs):

        # training loop
        for epoch in range(0, epochs):
            # observation loop
            for observation in self.dataset:
                
                # zero gradients
                self.optim.zero_grad()

                # get data and forward pass
                input, ground_truth = self.prepare_data(observation)
                inference = self.model.forward(input)

                # calculate loss
                loss = self.loss(inference, ground_truth)   

                # lackpropagate
                loss.backwards()

                # step
                self.optim.step()
        
        # save model
        torch.save(self.model.parameters(), f='epoch_{epoch}_saved_model')



    def prepare_data(self, observation):
        turbine_type_embedding = self.embeddings_Tensor[find_embeddings(observation[0], self.turbine_types)]
        input  = torch.tensor([turbine_type_embedding[0], turbine_type_embedding[1], turbine_type_embedding[2], float(observation[1]), float(observation[2])], dtype=torch.float32)
        ground_truth = torch.tensor(float(observation[3]))
        return input, ground_truth

        


trainer = train_model(0.1)
trainer.train(1)