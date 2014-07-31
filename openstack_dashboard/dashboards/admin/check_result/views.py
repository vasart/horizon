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

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables

from openstack_dashboard import api

from openstack_dashboard.dashboards.admin.check_result \
    import tables as project_tables


INDEX_URL = "horizon:admin:check_result:index"

class Result():
    def __init__(self, result_api):
        self.id = result_api.id
        self.time = result_api.time
        self.name = result_api.name
        self.node = result_api.node
        if int(result_api.result) == 0:
            self.result = 'not_trusted'
        elif int(result_api.result) == 1:
            self.result = 'trusted'
        else:
            self.result = 'unknown'
        self.status = result_api.status

class IndexView(tables.DataTableView):
    table_class = project_tables.CheckTable
    template_name = 'admin/check_result/index.html'

    def get_data(self):
        request = self.request
        results = []
        try:
            # results = api.nova.flavor_list(request, None)            
            results_api = api.nova.periodic_checks_result_list(request)
            for result_api in results_api:
                results.append(Result(result_api))
        except Exception:
            exceptions.handle(request,
                              _('Unable to retrieve result list.'))
        return results
