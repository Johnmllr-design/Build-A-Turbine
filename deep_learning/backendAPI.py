from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from fastapi import Request
import numpy
from model import TurbinePredictionModel
import uvicorn


app = FastAPI()
TurbineModel = TurbinePredictionModel() # load in with torch.load eventually
model = TurbinePredictionModel()
state = torch.load('model_weights.pt')
model.load_state_dict(state)
embeddings_Tensor = torch.load('type_embeddings.pt')
turbine_types = numpy.load('turbine_types.npy')


app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TurbineObject(BaseModel):
    type : str
    longitude : float
    latitude : float


@app.post("/prediction")
def Request(req : TurbineObject):
    input = [req.type, req.latitude, req.longitude]
    input = torch.tensor(input, dtype=torch.float32)
    model.eval()
    inference = model.forward(input)
    prediction = str(inference.item())[0:8] + " kWh per day"
    return {"returnedVal" : prediction}


if __name__ == "__main__":
    uvicorn.run("backendAPI:app", host="127.0.0.1", port=8000, reload=True)
    



    

