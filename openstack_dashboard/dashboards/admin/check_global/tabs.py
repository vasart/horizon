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

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api

from openstack_dashboard.dashboards.admin.check_global import constants
from openstack_dashboard.dashboards.admin.check_global import tables



class SecurityChecksLogsTab(tabs.TableTab):
    table_classes = (tables.SecurityChecksLogsTable,)
    name = _("Security Checks Logs")
    slug = "security_checks_logs"
    template_name = constants.INFO_DETAIL_TEMPLATE_NAME

    def get_security_checks_logs_data(self):
        log_records = api.nova.periodic_checks_log(self.request)
        return log_records


class SecurityChecksOptionsTab(tabs.TableTab):
    table_classes = (tables.SecurityChecksOptionsTable,)
    name = _("Security Checks Options")
    slug = "security_checks_options"
    template_name = constants.INFO_DETAIL_TEMPLATE_NAME

    def get_security_checks_options_data(self):
        options = api.nova.periodic_checks_options(self.request)
        return options


class SecurityChecksSettingsTabs(tabs.TabGroup):
    slug = "security_checks_settings"
    tabs = (SecurityChecksLogsTab, SecurityChecksOptionsTab)
    sticky = True
