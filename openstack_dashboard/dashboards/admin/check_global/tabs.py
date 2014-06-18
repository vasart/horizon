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

from openstack_dashboard.api import nova

from openstack_dashboard.dashboards.admin.check_global import constants
from openstack_dashboard.dashboards.admin.check_global import tables
from logging import LogRecord


class LogRecord(object):
    def __init__(self, record_id, log_record_time, log_record_source, log_record_message):
        self.id = record_id
        self.log_record_time = log_record_time
        self.log_record_source = log_record_source
        self.log_record_message = log_record_message


class Option(object):
    def __init__(self, name, value):
        self.id = name
        self.value = value


class SecurityChecksLogsTab(tabs.TableTab):
    table_classes = (tables.SecurityChecksLogsTable,)
    name = _("Security Checks Logs")
    slug = "security_checks_logs"
    template_name = constants.INFO_DETAIL_TEMPLATE_NAME

    def get_security_checks_logs_data(self):
        log_records = []
        log_records.append(LogRecord("1", "12345", "source1", "message1"))
        log_records.append(LogRecord("2", "12312", "source2", "message2"))
        return log_records


class SecurityChecksOptionsTab(tabs.TableTab):
    table_classes = (tables.SecurityChecksOptionsTable,)
    name = _("Security Checks Options")
    slug = "security_checks_options"
    template_name = constants.INFO_DETAIL_TEMPLATE_NAME

    def get_security_checks_options_data(self):
        options = []
        options.append(Option("Security Checks Enabled", True))
        options.append(Option("Clean Tcp When Down", True))
        options.append(Option("OpenAttestation Location", "192.168.255.4"))
        return options


class SecurityChecksSettingsTabs(tabs.TabGroup):
    slug = "security_checks_settings"
    tabs = (SecurityChecksLogsTab, SecurityChecksOptionsTab)
    sticky = True
