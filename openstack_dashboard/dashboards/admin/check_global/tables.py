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

from openstack_dashboard import api


ENABLE = 0
DISABLE = 1


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


class ToggleEnabled(tables.BatchAction):
    name = "toggle"
    action_present = (_("Enable"), _("Disable"))
    action_past = (_("Enabled"), _("Disabled"))
    data_type_singular = _("Option")
    data_type_plural = _("Options")
    classes = ("btn-toggle",)
    policy_rules = (('identity', 'admin_required'),)

    def get_policy_target(self, request, option=None):
        if option:
            return {"option_id": option.id}
        return {}

    def allowed(self, request, option=None):
        self.enabled = True
        if not option:
            return self.enabled
        self.enabled = option.enabled
        if self.enabled:
            self.current_present_action = DISABLE
        else:
            self.current_present_action = ENABLE
        return True

#     def update(self, request, option=None):
#         super(ToggleEnabled, self).update(request, option)
#         if option and option.id == request.option.id:
#             self.attrs["disabled"] = "disabled"

    def action(self, request, obj_id):
        if self.enabled:
            api.nova.option_update_enabled(request, obj_id, False)
            self.current_past_action = DISABLE
        else:
            api.nova.option_update_enabled(request, obj_id, True)
            self.current_past_action = ENABLE


class SecurityChecksOptionsTable(tables.DataTable):
    name = tables.Column("id", verbose_name=_('Name'))
    value = tables.Column('enabled', verbose_name=_('Enabled'))

    class Meta:
        name = "security_checks_options"
        verbose_name = _("Security Checks Options")
        table_actions = (SecurityChecksOptionsFilterAction,)
        multi_select = False
        row_actions = (ToggleEnabled,)
