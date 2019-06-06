from typing import NamedTuple, Optional, Dict

import aiohttp
from isppyapi.manager import ManagerClient

VDS = NamedTuple('VDS', fields=[('createdate', str),
                                ('domain', str),
                                ('name', str),
                                ('ip', str)])


class BillManagerClient(ManagerClient):
    def __init__(self,
                 session: Optional[aiohttp.ClientSession] = None,
                 base_url: str = ''):
        super().__init__(session, base_url)

    async def login(self, username: str, password: str) -> None:
        params = {
            'out': 'json',
            'func': 'auth',
            'username': username,
            'password': password
        }
        async with self._session.get(self.base_url, params=params) as response:
            result = await self._handle_response(response)
            self._session_id = result['doc']['auth']['$id']

    async def list_vds(self) -> Dict:
        params = {
            'out': 'json',
            'func': 'vds',
            'auth': self._session_id
        }
        async with self._session.get(self.base_url, params=params) as response:
            result = await self._handle_response(response)
            return result


