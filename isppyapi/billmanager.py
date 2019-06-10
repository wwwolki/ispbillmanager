from typing import NamedTuple, Optional, List
from pprint import pprint
import aiohttp
from isppyapi.manager import ManagerClient, extract_list

VDS = NamedTuple('VDS', fields=[('createdate', str),
                                ('domain', str),
                                ('name', str),
                                ('ip', str)])


class BillManagerClient(ManagerClient):
    def __init__(self,
                 session: Optional[aiohttp.ClientSession] = None,
                 base_url: str = ''):
        super().__init__(session, base_url)

    async def list_vds(self) -> List[VDS]:
        params = {
            'out': 'json',
            'func': 'vds',
            'auth': self._session_id
        }
        async with self._session.get(self.base_url, params=params) as response:
            response = await self._handle_response(response)
            return _extract_list(response, VDS)


