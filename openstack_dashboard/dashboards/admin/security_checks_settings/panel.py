from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.admin import dashboard


class SecurityChecksSettings(horizon.Panel):
    name = _("Security Checks Settings")
    slug = "security_checks_settings"


dashboard.Admin.register(SecurityChecksSettings)
