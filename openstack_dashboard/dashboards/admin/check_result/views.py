#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables
from horizon import workflows

from openstack_dashboard import api

from openstack_dashboard.dashboards.admin.check_result \
    import tables as project_tables
from openstack_dashboard.dashboards.admin.check_result \
    import workflows as flavor_workflows


INDEX_URL = "horizon:admin:check_result:index"


#change when nova part done

class IndexView(tables.DataTableView):
    table_class = project_tables.CheckTable
    template_name = 'admin/check_result/index.html'

    def get_data(self):
        request = self.request
        results = []
        try:
            # "is_public=None" will return all flavors.
           # results = api.nova.flavor_list(request, None)
            results = api.nova.result_list(request, None)
            print results
            # for i in range(len(results)):
            #     print results[i]
        except Exception:
            exceptions.handle(request,
                              _('Unable to retrieve result list.'))
        return results