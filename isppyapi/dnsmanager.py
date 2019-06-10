from typing import Optional, NamedTuple, List

from pprint import pprint
import aiohttp
from isppyapi.manager import extract_list
from isppyapi.manager import ManagerClient


Domain = NamedTuple('VDS', fields=[
    ('active', str),
    ('curruser', str),
    ('dnssecstatus', str),
    ('dtype', str),
    ('name', str),
    ('published', str),
    ('user', str)
])


DomainRecord = NamedTuple('DomainRecord', fields=[
    ('name', str),
    ('rkey', str),
    ('rkey_name', str),
    ('rtype', str),
    ('rtype_hidden', str),
    ('ttl', str),
    ('value', str)
])


class DnsManagerClient(ManagerClient):
    def __init__(self,
                 session: Optional[aiohttp.ClientSession] = None,
                 base_url: str = ''):
        super().__init__(session, base_url)

    async def list_domains(self) -> List[Domain]:
        params = {
            'out': 'json',
            'func': 'domain',
            'auth': self._session_id
        }
        async with self._session.get(self.base_url, params=params) as response:
            response = await self._handle_response(response)
            return extract_list(response, Domain)

    async def domain_su(self)->dict:
        params = {
            'out': 'json',
            'func': 'domain.su',
            'auth': self._session_id,
        }
        async with self._session.get(self.base_url, params=params) as response:
            result = await self._handle_response(response)
            return result

    async def list_domain_records(self, name)->List[DomainRecord]:
        params = {
            'out': 'json',
            'func': 'domain.record',
            'auth': self._session_id,
            'elname': name,
            'elid': name,
        }
        async with self._session.get(self.base_url, params=params) as response:
            result = await self._handle_response(response)
            return extract_list(result, DomainRecord)

    async def add_domain_record(self, domain_name, name, ip)->dict:
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

    async def remove_record(self, domain, rkeys)->dict:
        params = {
            'out': 'json',
            'func': 'domain.record.delete',
            'auth': self._session_id,
            'elid': rkeys,
            'plid': domain,
            'sok': 'ok',
        }
        pprint(params)
        async with self._session.get(self.base_url, params=params) as response:
            result = await self._handle_response(response)
            return result