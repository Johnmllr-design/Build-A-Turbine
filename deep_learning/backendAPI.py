from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from fastapi import Request
import numpy
from model import TurbinePredictionModel
import uvicorn
from utils import normalize_input
from utils import normalize_input_2
from utils import de_normalize_output



app = FastAPI()

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




TurbineModel = TurbinePredictionModel() # load in with torch.load eventually
model = TurbinePredictionModel()
state = torch.load('model_weights.pt')
model.load_state_dict(state)
embeddings_Tensor = torch.load('type_embeddings.pt')
turbine_types = numpy.load('turbine_types.npy')

@app.post("/prediction")
def Request(req : TurbineObject):
    print(req.model_dump())
    input = [req.type, req.latitude, req.longitude]
    input = torch.tensor(normalize_input_2(input), dtype=torch.float32)
    print("inference input is " + str(input))
    model.eval()
    inference = model.forward(input)
    prediction = str(de_normalize_output(inference.item()))[0:8] + " kWh per day"
    return {"returnedVal" : prediction}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backendAPI:app", host="127.0.0.1", port=8000, reload=True)
    



    

