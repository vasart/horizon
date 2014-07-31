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


class SecurityChecksLogsFilterAction(tables.FilterAction):
    def filter(self, table, log_records, filter_string):
        q = filter_string.lower()

        def comp(log_record):
            if q in log_record.type.lower():
                return True
            return False

        return filter(comp, log_records)


def get_enabled(service, reverse=False):
    options = ["Enabled", "Disabled"]
    if reverse:
        options.reverse()
    # if not configured in this region, neither option makes sense
    if service.host:
        return options[0] if not service.disabled else options[1]
    return None


class SecurityChecksLogsTable(tables.DataTable):
    id = tables.Column('id', hidden=True)
    log_record_time = tables.Column('log_record_time',
        verbose_name=_('Log Record Time'))
    log_record_source = tables.Column('log_record_source',
        verbose_name=_('Log Record Source'))
    log_record_message = tables.Column('log_record_message',
        verbose_name=_('Log Record Message'), status=True)

    class Meta:
        name = "security_checks_logs"
        verbose_name = _("Security Checks Logs")
        table_actions = (SecurityChecksLogsFilterAction,)
        multi_select = False