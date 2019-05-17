# Cloud watch

List virtual machines in the cloud (currently only openstack supported)

# Install

```bash
$ pip install git+https://github.com/viklund/cloud-watch.git
```

# Configure

Create the file `$HOME/.config/cloud-watch/settings.yml` and edit it, here's a
sample for SSC:

```yaml
SSC:
    type: openstack
    password: <password>
    user: <user>
    domain: snic
    projects:
        - SNIC 2018/10-20
    regions:
        - name: HPC2N
          auth_url: https://hpc2n.cloud.snic.se:5000
          version: 3.x_password
        - name: UPPMAX
          auth_url: https://uppmax.cloud.snic.se:5000
          version: 3.x_password
        - name: C3SE
          auth_url: https://c3se.cloud.snic.se:5000
          version: 3.x_password
```
