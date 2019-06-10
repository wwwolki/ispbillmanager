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
    parser.add_argument('args', nargs='*')
    parser.add_argument('-c', '--config', default='config.ini', help="config filename")
    args = parser.parse_args()

    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))

    config = configparser.ConfigParser()
    config.read(args.config)

    async with session:
        username = args.user or config[args.manager]['user']
        password = args.password or config[args.manager]['password']
        base_url = config[args.manager]['base_url']
        manager = MANAGERS[args.manager](session, base_url=base_url)
        await manager.login(username=username, password=password)

        if args.command == 'list':
            result = await manager.list_vds()
            for vds in result:
                print(vds)
        if args.command == 'list_domains':
            result = await manager.list_domains()
            pprint(result)
        if args.command == 'domain_su':
            result = await manager.domain_su()
            pprint(result)

        if args.command == 'list_records':
            result = await manager.list_domain_records(*args.args)
            pprint(result)

        if args.command == 'add_record':
            result = await manager.add_domain_record(*args.args)
            pprint(result)

        if args.command == 'remove_record':
            result = await manager.remove_record(*args.args)
            pprint(result)
        """
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
