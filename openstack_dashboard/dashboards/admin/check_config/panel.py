from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.admin import dashboard


class Check_Config(horizon.Panel):
    name = _("Configuration")
    slug = "check_config"


dashboard.Admin.register(Check_Config)
