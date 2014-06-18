from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.admin import dashboard


class Check_Result(horizon.Panel):
    name = _("Results")
    slug = "check_result"


dashboard.Admin.register(Check_Result)
