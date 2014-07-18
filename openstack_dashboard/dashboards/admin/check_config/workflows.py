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


class AddCheckInfoAction(workflows.Action):
    name = forms.RegexField(label=_("Name"),
                            max_length=255,
                            regex=r'^[\w\.\- ]+$',
                            error_messages={'invalid': _('Name may only '
                                'contain letters, numbers, underscores, '
                                'periods and hyphens.')})

    desc = forms.CharField(label=_("Description"))
    timeout = forms.IntegerField(label=_("Timeout"), min_value=1)
    spacing = forms.IntegerField(label=_("Spacing"), min_value=1)

    class Meta:
        name = _("Check Info")
        help_text = _("From here you can add a new check.")

    def clean(self):
        cleaned_data = super(AddCheckInfoAction, self).clean()
        name = cleaned_data.get('name')

        try:
            checks = api.nova.periodic_checks_list(self.request)
        except Exception:
            checks = []
            msg = _('Unable to get checks list')
            exceptions.check_message(["Connection", "refused"], msg)
            raise
        if checks is not None:
            for check in checks:
                if check.name == name:
                    raise forms.ValidationError(
                        _('The name "%s" is already used by another check.')
                        % name
                    )
        return cleaned_data


class UpdateCheckInfoAction(workflows.Action):
    check_id = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.RegexField(label=_("Name"),
                            max_length=255,
                            regex=r'^[\w\.\- ]+$',
                            error_messages={'invalid': _('Name may only '
                                'contain letters, numbers, underscores, '
                                'periods and hyphens.')})
    desc = forms.CharField(label=_("Description"))
    timeout = forms.IntegerField(label=_("Timeout"),
                            min_value=1)
    spacing = forms.IntegerField(label=_("Spacing"),
                            min_value=1)

    class Meta:
        name = _("Check Info")
        help_text = _("From here you can edit a check.")


class AddCheckInfo(workflows.Step):
    action_class = AddCheckInfoAction
    contributes = ("check_id",
                   "name",
                   "desc",
                   "timeout",
                   "spacing",
                   )


class AddCheck(workflows.Workflow):
    slug = "add_check"
    name = _("Add Check")
    finalize_button_name = _("Add Check")
    success_message = _('Added new check "%s".')
    failure_message = _('Unable to add check "%s".')
    success_url = "horizon:admin:check_config:index"
    default_steps = (AddCheckInfo,)

    def format_status_message(self, message):
        return message % self.context['name']

    def handle(self, request, data):
        # Add new check
        # check_id = data.get('check_id') or 'auto'
        try:
            self.object = api.nova.periodic_check_create(request,
                                                    name=data['name'],
                                                    desc=data['desc'],
                                                    timeout=data['timeout'],
                                                    spacing=data['spacing'],)
        except Exception:
            exceptions.handle(request, _('Unable to add new check.'))
            return False

        return True


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
            check_id = data['check_id']
            api.nova.periodic_check_delete(request, check_id)
            api.nova.periodic_check_create(request,
                                           name=data['name'],
                                           desc=data['desc'],
                                           timeout=data['timeout'],
                                           spacing=data['spacing'],
                                           )
        except Exception:
            exceptions.handle(request, ignore=True)
            return False
        return True
