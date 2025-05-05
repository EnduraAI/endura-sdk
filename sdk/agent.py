import psutil

class DeviceAgent:
    def __init__(self, model):
        self.model = model

    def get_status(self):
        return {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent
        }