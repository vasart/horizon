# Copyright 2013 B1 Systems GmbH
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


from django.utils.translation import ugettext_lazy as _

from horizon import tables
from openstack_dashboard.dashboards.admin.check_global import constants


def get_enabled(service, reverse=False):
    options = ["Enabled", "Disabled"]
    if reverse:
        options.reverse()
    # if not configured in this region, neither option makes sense
    if service.host:
        return options[0] if not service.disabled else options[1]
    return None

class SecurityChecksOptionsFilterAction(tables.FilterAction):
    def filter(self, table, options, filter_string):
        q = filter_string.lower()

        def comp(option):
            if q in option.type.lower():
                return True
            return False

        return filter(comp, options)


class EditOption(tables.LinkAction):
    name = "edit_option"
    verbose_name = _("Edit Option")
    url = "horizon:admin:check_global:update"
    classes = ("ajax-modal", "btn-edit")
    policy_rules = (('identity', 'admin_required'),)

    def allowed(self, request, datum):
        opt_id = request.session.get("option_id", None)
        return opt_id is not "oa_address"

    def single(self, table, request, obj_id):
        return


class SecurityChecksOptionsTable(tables.DataTable):
    name = tables.Column("id", verbose_name=_('Name'))
    value = tables.Column('value', verbose_name=_('Value'))

    class Meta:
        name = "security_checks_options"
        verbose_name = _("Security Checks Options")
        table_actions = (SecurityChecksOptionsFilterAction,)
        multi_select = False
        row_actions = (EditOption,)
