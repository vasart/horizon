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

from openstack_dashboard.dashboards.admin.check_global import constants
from openstack_dashboard.dashboards.admin.check_global \
    import tables as project_tables

class Option():
    id_mapto_name = {"periodic_checks_enabled": "Periodic Checks Enabled",
                     "trusted_pool_saved": "Trusted Pool is Saved When Going Down"}
    def __init__(self, option_api):
        self.id = option_api.id
        self.name = Option.id_mapto_name[option_api.id]
        self.value = option_api.value

class IndexView(tables.DataTableView):
    table_class = project_tables.SecurityChecksOptionsTable
    name = "Security Checks Options"
    slug = "security_checks_options"
    template_name = constants.INFO_TEMPLATE_NAME

    def get_data(self):
        options = []
        options_api = api.nova.periodic_checks_options(self.request)
        for option in options_api:
            options.append(Option(option))
        return options
