from typing import Optional, Dict, List, Any

import aiohttp


class BaseError(Exception):
    """ Base exception for all managers """


class BadCode(BaseError):
    """ A wrapper for non-200 response """


class UnknownError(BaseError):
    """ Something nasty happened and we don't know what to do """
    def __init__(self, text):
        super().__init__("api returned an unknown error: {}".format(text))


class ApiError(BaseError):
    """ This is the only exception which should be handled and subclassed """
    def __init__(self, error_description):
        super().__init__('api returned error:{}'.format(error_description))


def extract_list(doc, elemType) -> List[Any]:
    result = []
    for doc in doc['elem']:
        vds = elemType(**{key: doc[key]['$'] for key in elemType._field_types.keys()})
        result.append(vds)
    return result


class ManagerClient:
    def __init__(self,
                 session: Optional[aiohttp.ClientSession] = None,
                 base_url: str = ''):
        self.base_url = base_url
        self._session = session or aiohttp.ClientSession()
        self._session_id = None

    async def _handle_response(self,
                               response: aiohttp.ClientResponse) -> Dict:

        """
            https error codes are not used in this api, so we can safely assume
            that something is very broken if we've got a non-200 response
            for now we do not retry on  429 and 500s
        """
        try:
            response.raise_for_status()
        except aiohttp.ClientError as exc:
            raise BadCode() from exc

        try:
            data = await response.json()
        except ValueError:
            raise UnknownError(await response.text())
        if "doc" not in data:
            raise UnknownError(str(data))
        if "error" in data["doc"]:
            error = data["doc"]["error"]["msg"]["$"]
            raise ApiError(error)
        return data['doc']

    async def login(self, username: str, password: str)->None:
        params = {
            'out': 'json',
            'func': 'auth',
            'username': username,
            'password': password
        }
        async with self._session.get(self.base_url, params=params) as response:
            result = await self._handle_response(response)
            print(result)
            self._session_id = result['auth']['$id']
