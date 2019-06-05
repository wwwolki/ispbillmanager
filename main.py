import asyncio
import argparse
import aiohttp
import configparser

from pprint import pprint
from isppyapi import billmanager

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user')
    parser.add_argument('--password')
    args = parser.parse_args()

    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))

    config = configparser.ConfigParser()
    config.read('config.ini')

    async with session:
        """
        manager = BillManagerClient(session)
        await manager.login(args.user, args.password)
        result = await manager.list_vds()
        for doc in result['doc']['elem']:
            vds = VDS(**{key: doc[key]['$'] for key in VDS._field_types.keys()})
            #print(vds)
            print(doc)
        """

        manager = billmanager.DnsManagerClient(session)
        await manager.login(config['dnsmanager']['user'],
                            config['dnsmanager']['password'])

        result = await manager.list_domains()
        pprint(result['doc']['elem'])
        for elem in result['doc']['elem']:
            name = elem['name']['$']
            r = await manager.add_domain_record(name, 'google', '8.8.8.8')
            pprint(r['doc'])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
