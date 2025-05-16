from fastapi import FastAPI
from sdk.agent import DeviceAgent
import torch
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)

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

@app.get("/post_status")
def post_status():
    return agent.post_status()