from django.core.urlresolvers import reverse_lazy


from horizon import tables


from openstack_dashboard import api


from openstack_dashboard.dashboards.admin.check_logs import constants
from openstack_dashboard.dashboards.admin.check_logs import tables as project_tables


class IndexView(tables.DataTableView):
    table_class = project_tables.SecurityChecksLogsTable
    name = ("Security Checks Logs")
    slug = "security_checks_logs"
    template_name = constants.INFO_TEMPLATE_NAME

    def get_data(self):
        log_records = api.nova.periodic_checks_log(self.request)
        return log_records
