from typing import NamedTuple

import aiohttp

from isppyapi.helpers import _handle_billmgr_response

VDS = NamedTuple('VDS', fields=[('createdate', str),
                                ('domain', str),
                                ('name', str),
                                ('ip', str)])


class BillManagerClient:

    BASE_URL = 'https://my.firstvds.ru/billmgr'

    def __init__(self, session=None, base_url=''):
        self._session = session or aiohttp.ClientSession()
        self._session_id = None

    async def login(self, username: str, password: str)->None:
        params = {
            'out': 'json',
            'func': 'auth',
            'username': username,
            'password': password
        }
        async with self._session.get(self.BASE_URL, params=params) as response:
            result = await _handle_billmgr_response(response)
            self._session_id = result['doc']['auth']['$id']

    async def list_vds(self)->dict:
        params = {
            'out': 'json',
            'func': 'vds',
            'auth': self._session_id
        }
        async with self._session.get(self.BASE_URL, params=params) as response:
            result = await _handle_billmgr_response(response)
            return result


