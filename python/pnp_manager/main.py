# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


class PnPDevice(Service):
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        vars = ncs.template.Variables()
        template = ncs.template.Template(service)
        for rolename in service.role:
            # This will use the last role with PnP infor in the devices roles.
            # Need to modify the service model to restrict to only one role
            # with PnP info 
            role = root.device_role[rolename]
            if role.pnp.authgroup is not None:
                vars.add('AUTHGROUP', role.pnp.authgroup)
            if role.pnp.username is not None:
                vars.add('USERNAME', role.pnp.username)
            if role.pnp.port is not None:
                vars.add('PORT', role.pnp.port)
            if role.pnp.day0_file is not None:
                vars.add('DAY0-FILE', role.pnp.day0_file)

        if service.authgroup is not None:
            vars.add('AUTHGROUP', service.authgroup)
        if service.username is not None:
            vars.add('USERNAME', service.username)
        if service.port is not None:
            vars.add('PORT', service.port)
        if service.day0_file is not None:
            vars.add('DAY0-FILE', service.day0_file)

        template.apply('pnp-manager-device-pnp-map', vars)

class Main(ncs.application.Application):
    def setup(self):
        self.log.info('Main RUNNING')
        self.register_service('pnp-device-servicepoint', PnPDevice)

    def teardown(self):
        self.log.info('Main FINISHED')
