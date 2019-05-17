from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

import sys
from pathlib import Path

import yaml
from datetime import datetime
from tabulate import tabulate
import pytz

NOW = datetime.now(pytz.timezone('Europe/Stockholm'))
CONFIG_FILE_LOCATION = Path( Path.home(), '.config', 'cloud-watch', 'settings.yml')


class Tenant(object):
    def __init__(self, user, password, tenant, domain, auth_url, region, version):
        self.user = user
        self.password = password
        self.tenant = tenant
        self.domain = domain
        self.auth_url = auth_url
        self.region = region
        self.version = version

    @classmethod
    def create(cls, config):
        ts = []
        for cloud, info in config.items():
            if cloud != 'SSC':
                continue
            for p in info['projects']:
                for r in info['regions']:
                    ts.append(
                            Tenant(
                                user     = info['user'],
                                password = info['password'],
                                tenant   = p,
                                domain   = info['domain'],
                                auth_url = r['auth_url'],
                                region   = r['name'],
                                version  = r['version']
                                )
                            )
        return ts

    @property
    def driver(self):
        os = get_driver(Provider.OPENSTACK)
        return os(self.user,
                    self.password,
                    ex_tenant_name=self.tenant,
                    ex_domain_name=self.domain,
                    ex_force_auth_url=self.auth_url,
                    ex_force_service_region=self.region,
                    ex_force_auth_version=self.version,
                    )

    def get_nodes(self):
        info = []
        for n in self.driver.list_nodes():
            # private_ips, public_ips
            age = NOW - n.created_at
            key = n.extra['key_name']

            info.append([self.tenant, self.region, n.name, n.state, age.days, n.created_at, ', '.join(n.public_ips), key])
        return info


def _load_config():
    if not CONFIG_FILE_LOCATION.exists():
        if not CONFIG_FILE_LOCATION.parent.exists():
            CONFIG_FILE_LOCATION.parent.mkdir()
        print(f"Can't find config file: {CONFIG_FILE_LOCATION}")
        sys.exit(1)
    stat = CONFIG_FILE_LOCATION.stat()
    if stat.st_mode & 0o600 != 0o600:
        print(f"Config file don't have the correct permissions (0600)")
        sys.exit(1)
    with open(CONFIG_FILE_LOCATION) as fh:
        return yaml.load(fh, Loader=yaml.SafeLoader)


def main():
    config = _load_config()
    ts = Tenant.create(config)
    tasks = []
    info = []
    for tenant in ts:
        print(tenant.tenant)
        info.extend(tenant.get_nodes())
    print(tabulate(info, headers=['tenant', 'region', 'name', 'state', 'age (d)', 'created at', 'public ip', 'key'], tablefmt='simple'))

if __name__ == '__main__':
    main()
