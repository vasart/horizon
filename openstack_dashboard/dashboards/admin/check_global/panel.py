from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.admin import dashboard


class Check_Global(horizon.Panel):
    name = _("Settings")
    slug = "check_global"


dashboard.Admin.register(Check_Global)
