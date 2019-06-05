from typing import NamedTuple

import aiohttp


async def _handle_billmgr_response(response: aiohttp.ClientResponse) -> dict:
    if not response.status == 200:
        raise ValueError("""Billmgr api returned bad status code: {}""".format(response.status_code))
    try:
        data = await response.json()
    except ValueError:
        raise ValueError("""Billmgr api returned an unknown response: {}""".format(response.text))
    if "doc" not in data:
        raise ValueError("""Billmgr api returned an unknown error""")
    if "error" in data["doc"]:
        raise ValueError("""Billmgr returned an error: {}""".format(data["doc"]["error"]["msg"]["$"]))
    return data


VDS = NamedTuple('VDS', fields=[('createdate', str),
                                ('domain', str),
                                ('name', str),
                                ('ip', str)])


class BillManagerClient:

    BASE_URL = 'https://my.firstvds.ru/billmgr'

    def __init__(self, session=None):
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


