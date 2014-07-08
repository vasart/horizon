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

from horizon import tables

from openstack_dashboard import api


class DeleteResult(tables.DeleteAction):
    data_type_singular = _("Result")
    data_type_plural = _("Results")

    def delete(self, request, obj_id):
        #change when nova part done
        api.nova.flavor_delete(request, obj_id)


class ResultFilterAction(tables.FilterAction):
    def filter(self, table, results, filter_string):
        """Really naive case-insensitive search."""
        q = filter_string.lower()

        def comp(result):
            return q in result.name.lower()

        return filter(comp, results)


class CheckTable(tables.DataTable):
    time = tables.Column('time', verbose_name=_('Time'))
    name = tables.Column('name', verbose_name=_('Check Name'))
    node = tables.Column('node', verbose_name=_('Node Number'))
    results = tables.Column('result', verbose_name=_('Check Results'))

    class Meta:
        name = "results"
        verbose_name = _("Results")
        table_actions = (ResultFilterAction, DeleteResult)
        row_actions = (DeleteResult,)
