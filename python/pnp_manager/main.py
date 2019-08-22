# -*- mode: python; python-indent: 4 -*-
import _ncs
import ncs
import ncs.maapi as maapi
from ncs.application import Service


class PnPDevice(Service):
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        vars = ncs.template.Variables()
        template = ncs.template.Template(service)
        for servicerole in service.role:
            # This will use the last role with PnP info in the devices roles.
            # Need to modify the service model to restrict to only one role
            # with PnP info
            role = root.device_role[servicerole.name]
            if role.pnp.authgroup and role.pnp.day0_file:
                self.log.info("Processing role: "+servicerole.name)
                if role.pnp.authgroup is not None:
                    vars.add('AUTHGROUP', role.pnp.authgroup)
                    if root.devices.authgroups.group[role.pnp.authgroup].default_map.remote_name:
                        vars.add('USERNAME', root.devices.authgroups.group[role.pnp.authgroup].default_map.remote_name)
                    if root.devices.authgroups.group[role.pnp.authgroup].default_map.remote_password:
                        vars.add('PASSWORD', decrypt(root.devices.authgroups.group[role.pnp.authgroup].default_map.remote_password))
                if role.pnp.username is not None:
                    vars.add('USERNAME', role.pnp.username)
                if role.pnp.password is not None:
                    vars.add('PASSWORD', role.pnp.password)
                if role.pnp.port is not None:
                    vars.add('PORT', role.pnp.port)
                if role.pnp.day0_file is not None:
                    vars.add('DAY0-FILE', role.pnp.day0_file)

        # if service.authgroup is not None:
        #     vars.add('AUTHGROUP', service.authgroup)
        #     if root.devices.authgroups.group[service.authgroup].default_map.remote_name:
        #         vars.add('USERNAME', root.devices.authgroups.group[service.authgroup].default_map.remote_name)
        #     if root.devices.authgroups.group[service.authgroup].default_map.remote_password:
        #         vars.add('PASSWORD', decrypt(root.devices.authgroups.group[service.authgroup].default_map.remote_password))
        # if service.username is not None:
        #     vars.add('USERNAME', service.username)
        # if service.password is not None:
        #     vars.add('PASSWORD', service.password)
        # if service.port is not None:
        #     vars.add('PORT', service.port)
        # if service.day0_file is not None:
        #     vars.add('DAY0-FILE', service.day0_file)

        template.apply('pnp-manager-device-pnp-map', vars)

class Main(ncs.application.Application):
    def setup(self):
        self.log.info('Main RUNNING')
        self.register_service('pnp-device-servicepoint', PnPDevice)

    def teardown(self):
        self.log.info('Main FINISHED')

def decrypt(value):
    with maapi.Maapi() as m:
        m.install_crypto_keys()
    return _ncs.decrypt(value)