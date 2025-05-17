from fastapi import FastAPI
from endura_sdk import EnduraAgent, TestModel
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)

model = TestModel()
agent = EnduraAgent(model)

@app.get("/")
def read_root():
    return {"message": "Device API is running."}

@app.get("/status")
def get_status():
    return agent.get_status()

@app.get("/post_status")
def post_status():
    return agent.post_status()