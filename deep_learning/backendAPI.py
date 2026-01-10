from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Request
from model import TurbinePredictionModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class api():

    def __init__(self):
        self.TurbineModel = TurbinePredictionModel() # load in with torch.load eventually

    @app.get("/prediction")
    def Request(req:Request):
        pass

    

