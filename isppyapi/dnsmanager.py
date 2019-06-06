from typing import Optional

from pprint import pprint

import aiohttp

from isppyapi.manager import ManagerClient


class DnsManagerClient(ManagerClient):
    def __init__(self,
                 session: Optional[aiohttp.ClientSession] = None,
                 base_url: str = ''):
        super().__init__(session, base_url)

    async def login(self, username: str, password: str)->None:
        params = {
            'out': 'json',
            'func': 'auth',
            'username': username,
            'password': password
        }
        async with self._session.get(self.base_url, params=params) as response:
            result = await self._handle_response(response)
            self._session_id = result['doc']['auth']['$id']

    async def list_domains(self)->dict:
        params = {
            'out': 'json',
            'func': 'domain',
            'auth': self._session_id
        }
        async with self._session.get(self.base_url, params=params) as response:
            result = await self._handle_response(response)
            return result

    async def domain_su(self )->dict:
        params = {
            'out': 'json',
            'func': 'domain.su',
            'auth': self._session_id,
        }
        async with self._session.get(self.base_url, params=params) as response:
            result = await self._handle_response(response)
            return result

    async def list_domain_records(self, name)->dict:
        params = {
            'out': 'json',
            'func': 'domain.record',
            'auth': self._session_id,
            'elname': name,
            'elid': name,
        }
        async with self._session.get(self.base_url, params=params) as response:
            result = await self._handle_response(response)
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
        async with self._session.get(self.base_url, params=params) as response:
            result = await self._handle_response(response)
            return result