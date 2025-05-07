import psutil

def get_status(model):
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()

    return {
        "model_type": str(model.__class__.__name__),
        "cpu_usage": f"{cpu_percent}%",
        "memory_usage": f"{memory.percent}%"
    }