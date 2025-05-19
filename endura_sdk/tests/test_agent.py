from unittest.mock import AsyncMock, MagicMock
from endura_sdk.app.agent import DeviceAgent

def test_device_agent_initialization():
    agent = DeviceAgent()
    assert agent.status["health"] == "initializing"
    assert agent.model is None

def test_get_status_delegates_to_core(monkeypatch):
    fake_status = {"cpu": 50, "memory": 30}
    monkeypatch.setattr("endura_sdk.app.core.get_status", lambda model=None: fake_status)
    agent = DeviceAgent()
    assert agent.get_status() == fake_status

def test_log_inference_success():
    mock_model = MagicMock()
    mock_model.return_value.tolist.return_value = [1, 2, 3]
    mock_model.__call__.return_value = mock_model.return_value
    agent = DeviceAgent(mock_model)
    output = agent.log_inference("input")
    assert output.tolist() == [1, 2, 3]
    assert agent.status["last_output"] == [1, 2, 3]

def test_log_inference_error():
    class FailingModel:
        def __call__(self, x):
            raise ValueError("inference failed")
    agent = DeviceAgent(FailingModel())
    with pytest.raises(ValueError):
        agent.log_inference("input")
    assert "last_error" in agent.status

import pytest

@pytest.mark.asyncio
async def test_post_status(monkeypatch):
    agent = DeviceAgent()
    monkeypatch.setattr("endura_sdk.app.core.get_status", lambda model=None: {"mock": "status"})
    monkeypatch.setattr("endura_sdk.app.core.get_device_id", lambda: "abc-123")
    response_mock = AsyncMock()
    response_mock.raise_for_status.return_value = None
    response_mock.json.return_value = {"message": "ok"}
    response_mock.text = "ok"
    async_client_mock = AsyncMock()
    async_client_mock.__aenter__.return_value.put.return_value = response_mock
    monkeypatch.setattr("httpx.AsyncClient", lambda *a, **kw: async_client_mock)
    result = await agent.post_status()
    assert result == {"message": "ok"}