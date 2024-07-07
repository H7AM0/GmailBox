
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)
import aiohttp
import ssl
import certifi

class SessionManager:
    def __init__(self) -> None:
        self.session = None
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())

    async def create_session(self):
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(
            limit=50,
            ssl=self.ssl_context
        ))
        return self.session

    async def get_session(self):
        if self.session is None:
            self.session = await self.create_session()
            return self.session

        if self.session.closed:
            self.session = await self.create_session()

        if not self.session._loop.is_running():
            await self.session.close()
            self.session = await self.create_session()
        return self.session

session_manager = SessionManager()

async def make_request(url: str, method: str = "get", headers: dict = None, json: dict = None, timeout: int = 60, response_type: str = "json") -> dict:
    session = await session_manager.get_session()
    async with session.request(
        method=method.lower(),
        url=url,
        headers=headers,
        timeout=aiohttp.ClientTimeout(total=timeout),
        json=json,
    ) as response:
        if response_type == "text":
            return await response.text()
        elif response_type == "cookies":
            return {k: v.value for k, v in response.cookies.items()}
        else:
            return await response.json()
