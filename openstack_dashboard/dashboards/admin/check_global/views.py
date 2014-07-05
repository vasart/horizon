from django.core.urlresolvers import reverse_lazy


from horizon import tables

from openstack_dashboard import api

from openstack_dashboard.dashboards.admin.check_global import constants
from openstack_dashboard.dashboards.admin.check_global import tables as project_tables


class IndexView(tables.DataTableView):
    table_class = project_tables.SecurityChecksOptionsTable
    name = "Security Checks Options"
    slug = "security_checks_options"
    template_name = constants.INFO_TEMPLATE_NAME

    def get_data(self):
        options = api.nova.periodic_checks_options(self.request)
        return options
