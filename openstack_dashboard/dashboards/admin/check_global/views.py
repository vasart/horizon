from horizon import tabs

from openstack_dashboard.dashboards.admin.check_global import constants
from openstack_dashboard.dashboards.admin.check_global import tabs as project_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = project_tabs.SecurityChecksSettingsTabs
    template_name = constants.INFO_TEMPLATE_NAME
