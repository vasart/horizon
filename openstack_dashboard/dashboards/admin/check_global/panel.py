from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.admin import dashboard


class SecurityChecksSettings(horizon.Panel):
    name = _("Periodic Checks Settings")
    slug = "check_global"


dashboard.Admin.register(SecurityChecksSettings)
