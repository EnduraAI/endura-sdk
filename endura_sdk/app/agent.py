from endura_sdk.app.core import get_status, get_device_id
from endura_sdk.app import config
import httpx
import logging
import asyncio

logger = logging.getLogger(__name__)

class DeviceAgent:
    def __init__(self, model=None):
        self.model = model
        self.status = {"health": "initializing"}

    def get_status(self):
        return get_status(self.model)

    def update_status(self, new_status):
        self.status.update(new_status)

    def log_inference(self, input_data):
        if not self.model:
            raise ValueError("Model is not set. Cannot run inference.")
        try:
            output = self.model(input_data)
            self.update_status({"last_output": output.tolist()})
            return output
        except Exception as e:
            self.update_status({"last_error": str(e)})
            raise

    async def post_status(self):
        status = get_status(self.model)
        try:
            url = f"{config.BACKEND_URL.rstrip()}/status/{get_device_id()}"
            logger.debug(f"Posting status to {url}: {status}")
            async with httpx.AsyncClient() as client:
                response = await client.put(url, json=status)
            response.raise_for_status()
            logger.debug(f"Response from server: {response.text}")
            return response.json()
        except httpx.HTTPStatusError as e:
            error_text = await e.response.aread()
            logger.error(f"HTTP error {e.response.status_code} posting to {e.request.url}: {error_text}")
            return {
                "error": f"HTTP {e.response.status_code}",
                "url": str(e.request.url),
                "response": error_text.decode("utf-8")
            }
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            return {
                "error": str(e),
                "type": type(e).__name__
            }

    async def run_status_loop(self, interval=60):
        logger.info(f"Starting periodic status updates every {interval} seconds.")
        while True:
            result = await self.post_status()
            logger.info(f"Status update result: {result}")
            await asyncio.sleep(interval)