# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Try Docker first, then local
docker_env_path = Path("/app/.env")
local_env_path = Path(__file__).resolve().parent.parent.parent / ".env"

if docker_env_path.exists():
    load_dotenv(dotenv_path=docker_env_path)
else:
    load_dotenv(dotenv_path=local_env_path)

DEVICE_ID_FILE = os.getenv("DEVICE_ID_FILE", "/tmp/device_id.json")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
STATUS_LOOP_ENABLED = os.getenv("STATUS_LOOP_ENABLED", "false").lower() == "true"
API_KEY = os.getenv("ENDURA_API_KEY")