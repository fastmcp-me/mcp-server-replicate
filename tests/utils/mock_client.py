"""Mock client for testing Replicate API interactions."""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class MockResponse:
    """Mock HTTP response."""
    status_code: int
    json_data: Dict[str, Any]
    
    async def json(self) -> Dict[str, Any]:
        """Return JSON response data."""
        return self.json_data

class MockReplicateClient:
    """Mock Replicate API client for testing."""
    
    def __init__(self, responses: Dict[str, Any]) -> None:
        """Initialize mock client with predefined responses."""
        self.responses = responses
        self.calls: List[Dict[str, Any]] = []
        
    async def get_model(self, owner: str, name: str) -> MockResponse:
        """Mock get model endpoint."""
        self.calls.append({
            "method": "GET",
            "endpoint": f"models/{owner}/{name}",
            "timestamp": datetime.now(timezone.utc),
        })
        
        # Return first model from list response as default
        model = self.responses["models"]["list"]["results"][0]
        return MockResponse(200, model)
    
    async def create_prediction(
        self,
        version: str,
        input: Dict[str, Any],
        webhook: Optional[str] = None,
    ) -> MockResponse:
        """Mock create prediction endpoint."""
        self.calls.append({
            "method": "POST",
            "endpoint": "predictions",
            "data": {
                "version": version,
                "input": input,
                "webhook": webhook,
            },
            "timestamp": datetime.now(timezone.utc),
        })
        return MockResponse(201, self.responses["predictions"]["create"])
    
    async def get_prediction(self, id: str) -> MockResponse:
        """Mock get prediction endpoint."""
        self.calls.append({
            "method": "GET",
            "endpoint": f"predictions/{id}",
            "timestamp": datetime.now(timezone.utc),
        })
        return MockResponse(200, self.responses["predictions"]["get"])
    
    async def cancel_prediction(self, id: str) -> MockResponse:
        """Mock cancel prediction endpoint."""
        self.calls.append({
            "method": "POST",
            "endpoint": f"predictions/{id}/cancel",
            "timestamp": datetime.now(timezone.utc),
        })
        
        response = self.responses["predictions"]["get"].copy()
        response["status"] = "canceled"
        return MockResponse(200, response)
    
    def get_calls(self, method: Optional[str] = None, endpoint: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get filtered API calls."""
        filtered = self.calls
        if method:
            filtered = [c for c in filtered if c["method"] == method]
        if endpoint:
            filtered = [c for c in filtered if c["endpoint"] == endpoint]
        return filtered 