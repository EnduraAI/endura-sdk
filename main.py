from fastapi import FastAPI
from sdk.agent import DeviceAgent
import torch

app = FastAPI()

class TestModel(torch.nn.Module):
    def forward(self, x):
        return x * 2

model = TestModel()
agent = DeviceAgent(model)

@app.get("/")
def read_root():
    return {"message": "Device API is running."}

@app.get("/status")
def get_status():
    return agent.get_status()