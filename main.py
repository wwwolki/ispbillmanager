import asyncio
import argparse
import aiohttp
import configparser

from pprint import pprint

import isppyapi


MANAGERS = {
    'billmanager': isppyapi.BillManagerClient,
    'dnsmanager': isppyapi.DnsManagerClient
}

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user')
    parser.add_argument('--password')
    parser.add_argument('manager')
    parser.add_argument('command')
    parser.add_argument('-c', '--config', default='config.ini', help="config filename")
    args = parser.parse_args()

    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))

    config = configparser.ConfigParser()
    config.read(args.config)

    async with session:
        manager = MANAGERS[args.manager](session)
        username = args.user or config[args.manager]['user']
        password = args.password or config[args.manager]['password']
        await manager.login(username=username, password=password)

        """
        manager = isppyapi.BillManagerClient(session)
        await manager.login(args.user, args.password)
        result = await manager.list_vds()
        for doc in result['doc']['elem']:
            vds = isppyapi.VDS(**{key: doc[key]['$'] for key in VDS._field_types.keys()})
            #print(vds)
            print(doc)

        manager = isppyapi.DnsManagerClient(session, base_url=config['dnsmanager']['base_url'])
        await manager.login(config['dnsmanager']['user'],
                            config['dnsmanager']['password'])

        result = await manager.list_domains()
        pprint(result['doc']['elem'])
        for elem in result['doc']['elem']:
            name = elem['name']['$']
            r = await manager.add_domain_record(name, 'google', '8.8.8.8')
            pprint(r['doc'])
        """


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
