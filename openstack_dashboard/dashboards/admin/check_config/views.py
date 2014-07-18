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

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables
from horizon import workflows

from openstack_dashboard import api

from openstack_dashboard.dashboards.admin.check_config \
    import tables as check_tables
from openstack_dashboard.dashboards.admin.check_config \
    import workflows as check_workflows


INDEX_URL = "horizon:admin:check_config:index"


class IndexView(tables.DataTableView):
    table_class = check_tables.PeriodicChecksTable
    template_name = 'admin/check_config/index.html'

    def get_data(self):
        request = self.request
        checks = []
        try:
            checks = api.nova.periodic_checks_list(request)
        except Exception:
            exceptions.handle(request,
                              _('Unable to retrieve checks list.'))
        # Sort checks by name
        checks.sort(key=lambda f: (f.name))
        return checks


class AddView(workflows.WorkflowView):
    workflow_class = check_workflows.AddCheck
    template_name = 'admin/check_config/add.html'


class UpdateView(workflows.WorkflowView):
    workflow_class = check_workflows.UpdateCheck
    template_name = 'admin/check_config/update.html'

    def get_initial(self):
        check_id = self.kwargs['id']

        try:
            # Get initial periodic check information
            check = api.nova.periodic_check_get(self.request, check_id)
            f = open("/tmp/debug_horizon", "w")
            f.write(check_id)
            f.close()
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve check details.'),
                              redirect=reverse_lazy(INDEX_URL))
        return {
            'check_id': check.id,
            'name': check.name,
            'desc': check.desc,
            'timeout': check.timeout,
            'spacing': check.spacing,
        }


'''
class DetailsView(workflows.WorkflowView):
    workflow_class = check_workflows.DetailsCheck
    template_name = 'admin/check_config/details.html'
'''
