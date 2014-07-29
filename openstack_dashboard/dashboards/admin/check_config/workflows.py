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

from horizon import exceptions
from horizon import forms
from horizon import workflows

from openstack_dashboard import api


class UpdateCheckInfoAction(workflows.Action):
    check_id = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.RegexField(label=_("Name"),
                            max_length=255,
                            regex=r'^[\w\.\- ]+$',
                            error_messages={'invalid': _('Name may only '
                                'contain letters, numbers, underscores, '
                                'periods and hyphens.')},
                            widget=forms.TextInput(attrs={'readonly':'True'}))

    desc = forms.CharField(label=_("Description"),
                           help_text=_("Short description for the check."),
                           widget=forms.TextInput(attrs={'readonly':'True'}))
    spacing = forms.IntegerField(label=_("Period, seconds"),
                                 help_text=_("How much time should pass between two consecutive checks."),
                                 min_value=1)    
    timeout = forms.IntegerField(label=_("Timeout, seconds"),
                                 help_text=_("Timeout in seconds for waiting for the check result."),
                                 min_value=1)

    class Meta:
        name = _("Check Info")
        help_text = _("From here you can edit a check.")


class UpdateCheckInfo(workflows.Step):
    action_class = UpdateCheckInfoAction
    contributes = ("check_id",
                   "name",
                   "desc",
                   "timeout",
                   "spacing")


class UpdateCheck(workflows.Workflow):
    slug = "update_check"
    name = _("Edit Check")
    finalize_button_name = _("Save")
    success_message = _('Modified check "%s".')
    failure_message = _('Unable to modify check "%s".')
    success_url = "horizon:admin:check_config:index"
    default_steps = (UpdateCheckInfo,)

    def format_status_message(self, message):
        return message % self.context['name']

    def handle(self, request, data):
        # Update check information
        try:
            api.nova.periodic_check_update(request,
                                           name=data['name'],
                                           desc=data['desc'],
                                           timeout=data['timeout'],
                                           spacing=data['spacing'],
                                           check_id=data['check_id']
                                           )
        except Exception:
            exceptions.handle(request, ignore=True)
            return False
        return True
