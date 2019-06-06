from typing import Optional, Dict

import aiohttp


class ManagerClient:
    def __init__(self,
                 session: Optional[aiohttp.ClientSession] = None,
                 base_url: str = ''):
        self.base_url = base_url
        self._session = session or aiohttp.ClientSession()
        self._session_id = None

    async def _handle_response(self,
                               response: aiohttp.ClientResponse) -> Dict:

        if not response.status == 200:
            raise ValueError(self.__class__.__name__ + " api returned bad status code: {}".format(response.status_code))
        try:
            data = await response.json()
        except ValueError:
            raise ValueError(self.__class__.__name__ + " api returned an unknown response: {}".format(response.text))
        if "doc" not in data:
            raise ValueError(self.__class__.__name__ + " api returned an unknown error")
        if "error" in data["doc"]:
            raise ValueError(self.__class__.__name__ + " returned an error: {}".format(data["doc"]["error"]["msg"]["$"]))
        return data
