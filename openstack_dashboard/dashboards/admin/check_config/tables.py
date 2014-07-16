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

from django.utils.translation import ugettext_lazy as _

from horizon import tables

from openstack_dashboard import api


class DeleteCheck(tables.DeleteAction):
    data_type_singular = _("PeriodicCheck")
    data_type_plural = _("PeriodicChecks")

    def delete(self, request, obj_id):
        api.nova.periodic_check_delete(request, obj_id)


class AddCheck(tables.LinkAction):
    name = "add"
    verbose_name = _("Add Check")
    url = "horizon:admin:check_config:add"
    classes = ("ajax-modal", "btn-create")


class UpdateCheck(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit Check")
    url = "horizon:admin:check_config:update"
    classes = ("ajax-modal", "btn-edit")


class CheckFilterAction(tables.FilterAction):
    def filter(self, table, checks, filter_string):
        """Really naive case-insensitive search."""
        q = filter_string.lower()

        def comp(check):
            return q in check.name.lower()

        return filter(comp, checks)


class PeriodicChecksTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    desc = tables.Column('desc', verbose_name=_("Description"))
    timeout = tables.Column('timeout', verbose_name=_("Timeout"))
    spacing = tables.Column('spacing', verbose_name=_("Spacing"))
    
    class Meta:
        name = "checks"
        verbose_name = _("Periodic Checks")
        table_actions = (CheckFilterAction, AddCheck, DeleteCheck)
        row_actions = (UpdateCheck,
                       DeleteCheck)
