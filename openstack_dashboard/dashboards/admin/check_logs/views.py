# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from horizon import tables

from openstack_dashboard import api

from openstack_dashboard.dashboards.admin.check_logs import constants
from openstack_dashboard.dashboards.admin.check_logs \
    import tables as project_tables


class IndexView(tables.DataTableView):
    table_class = project_tables.SecurityChecksLogsTable
    name = ("Security Checks Logs")
    slug = "security_checks_logs"
    template_name = constants.INFO_TEMPLATE_NAME

    def get_data(self):
        log_records = api.nova.periodic_checks_log(self.request)
        return log_records
