import httpx
from typing import Optional, Dict, Any, List

class BaseAPI:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None
    ) -> Optional[Dict]:
        url = f"{self.base_url}{endpoint}"
        try:
            response = await self.client.request(
                method=method,
                url=url,
                params=params,
                json=json
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"Error in API request: {str(e)}")
        return None