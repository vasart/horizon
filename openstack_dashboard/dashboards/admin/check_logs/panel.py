from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.admin import dashboard


class SecurityChecksLogs(horizon.Panel):
    name = _("Periodic Checks Logs")
    slug = "check_logs"


dashboard.Admin.register(SecurityChecksLogs)
