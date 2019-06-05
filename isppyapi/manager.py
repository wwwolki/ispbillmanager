from typing import Optional

import aiohttp

class ManagerClient:
    def __init__(self,
                 session: Optional[aiohttp.ClientSession] = None,
                 base_url: str = ''):
        self.base_url = base_url
        self._session = session or aiohttp.ClientSession()
        self._session_id = None
