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
async def post_status():
    return await agent.post_status()

@app.on_event("startup")
async def startup_event():
    # Launch the status loop in the background
    import asyncio
    asyncio.create_task(agent.run_status_loop(interval=60))