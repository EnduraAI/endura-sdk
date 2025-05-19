from endura_sdk.app import config
import psutil
import time
import os
import uuid
import logging
import socket
import platform

logger = logging.getLogger(__name__)

def get_status(model):
    status = {
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "cpu": psutil.cpu_percent(interval=1),
        # "hostname": socket.gethostname(),
        # "os": platform.system(),
        # "arch": platform.machine(),
        # "os_version": platform.version(),
        # "disk_usage": f"{psutil.disk_usage('/').percent}%",
        # "uptime_seconds": int(time.time() - psutil.boot_time()),
        "memory": psutil.virtual_memory().percent
    }
    if model:
        status["model"] = get_model_metadata(model)
    return status

def get_model_metadata(model):
    return {
        "type": str(model.__class__.__name__),
        "framework": "pytorch",  # or detect dynamically later
        "version": getattr(model, '__version__', "1.0.0"),  # customizable
        "hash": "fake_hash_123abc"  # placeholder for checksum or git SHA
    }

def get_device_id():
    try:
        if os.path.exists(config.DEVICE_ID_FILE):
            with open(config.DEVICE_ID_FILE, 'r') as f:
                return f.read().strip()
        else:
            new_id = str(uuid.uuid4())
            with open(config.DEVICE_ID_FILE, 'w') as f:
                f.write(new_id)
            return new_id
    except OSError as e:
        logger.exception("Failed to get or create device ID")
        return str(uuid.uuid4())

def is_valid_device():
    cpu_arch = platform.machine()
    if cpu_arch not in {"armv7l", "aarch64"}:
        return False
    if os.getenv("IS_EDGE") != "true":
        return False
    return True