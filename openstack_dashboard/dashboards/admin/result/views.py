# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
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

from openstack_dashboard.dashboards.admin.result \
    import tables as project_tables
from openstack_dashboard.dashboards.admin.result \
    import workflows as flavor_workflows


INDEX_URL = "horizon:admin:result:index"


#change when nova part done

class IndexView(tables.DataTableView):
    table_class = project_tables.CheckTable
    template_name = 'admin/result/index.html'

    def get_data(self):
        request = self.request
        results = []
        try:
            # "is_public=None" will return all flavors.
            results = api.nova.flavor_list(request, None)
        except Exception:
            exceptions.handle(request,
                              _('Unable to retrieve flavor list.'))
        return results