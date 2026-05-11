import httpx

class BaseClient:
    """Async aiohttp/httpx wrapper to send requests to backend."""
    def __init__(self):
        self.client = httpx.AsyncClient()
    
    async def close(self):
        await self.client.aclose()
