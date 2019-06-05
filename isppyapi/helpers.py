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
