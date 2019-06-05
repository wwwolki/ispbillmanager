from pprint import pprint

import aiohttp

from isppyapi.billmanager import _handle_billmgr_response


class DnsManagerClient:
    BASE_URL = 'https://82.146.47.1/manager/dnsmgr'

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

    async def list_domains(self)->dict:
        params = {
            'out': 'json',
            'func': 'domain',
            'auth': self._session_id
        }
        async with self._session.get(self.BASE_URL, params=params) as response:
            result = await _handle_billmgr_response(response)
            return result

    async def domain_su(self )->dict:
        params = {
            'out': 'json',
            'func': 'domain.su',
            'auth': self._session_id,
        }
        async with self._session.get(self.BASE_URL, params=params) as response:
            result = await _handle_billmgr_response(response)
            return result

    async def list_domain_records(self, name)->dict:
        params = {
            'out': 'json',
            'func': 'domain.record',
            'auth': self._session_id,
            'elname': name,
            'elid': name,
        }
        async with self._session.get(self.BASE_URL, params=params) as response:
            result = await _handle_billmgr_response(response)
            return result

    async def add_domain_record(self, domain_name, name, ip)->dict:
        full_name = '{}.{}. A  {}'.format(name, domain_name, ip)
        params = {
            'out': 'json',
            'func': 'domain.record.edit',
            'auth': self._session_id,
            'plid': domain_name,
            'sok': 'ok',
            'name': name,
            'ip': ip
        }
        pprint(params)
        async with self._session.get(self.BASE_URL, params=params) as response:
            result = await _handle_billmgr_response(response)
            return result