from fastapi import FastAPI
import torch
from sdk.agent import DeviceAgent

app = FastAPI()

class TestModel(torch.nn.Module):
    def forward(self, x):
        return x * 2

model = TestModel()
agent = DeviceAgent(model)

@app.get("/")
def root():
    return {"message": "Device API is running."}

@app.get("/status")
def get_status():
    return agent.get_status()