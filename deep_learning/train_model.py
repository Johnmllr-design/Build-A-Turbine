from model import TurbinePredictionModel
import numpy
import torch
from utils import find_embeddings

class train_model():

    def __init__(self, learning_rate):
        self.model = TurbinePredictionModel()
        self.dataset = numpy.load('dataset_rawdata.npy')       # numpy dataset array
        self.embeddings_Tensor = torch.load('type_embeddings.pt')
        self.turbine_types = numpy.load('turbine_types.npy')
        self.optim = torch.optim.Adam(params=self.model.parameters(), lr=learning_rate)
        self.loss = torch.nn.MSELoss()


    def train(self, epochs):

        # set model to train
        self.model.train()

        # training loop
        for epoch in range(0, epochs):
            # observation loop
            print("epoch ", epoch)
            epoch_loss = 0
            for i, observation in enumerate(self.dataset):
                
                # zero gradients
                self.optim.zero_grad()

                # get data and forward pass
                input, ground_truth = self.prepare_data(observation)
                inference = self.model(input)
                if i % 20 == 0:
                    print("inference for " + str(input) + " is " + str(inference.item()) + " with GT " + str(ground_truth.item()))




                # calculate loss
                loss = self.loss(inference, ground_truth)
                epoch_loss += loss.item()  

                # backpropagate
                loss.backward()

                # step
                self.optim.step()
            print(epoch_loss)
        
        # save model
        torch.save(self.model.state_dict(), 'model_weights.pt')



    def prepare_data(self, observation):
        turbine_type_embedding = self.embeddings_Tensor[find_embeddings(observation[0], self.turbine_types)]
        input  = torch.tensor([turbine_type_embedding[0], turbine_type_embedding[1], turbine_type_embedding[2], float(observation[1]), float(observation[2])], dtype=torch.float32)
        ground_truth = torch.tensor([float(observation[3])])
        return input, ground_truth

        

if __name__ == '__main__':
    trainer = train_model(0.01)
    trainer.train(100)
