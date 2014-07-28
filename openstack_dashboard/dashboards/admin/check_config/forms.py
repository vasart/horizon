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
from django.core.files.base import ContentFile

"""
Views for managing images.
"""
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from openstack_dashboard import api
from openstack_dashboard import policy

import base64

class AddCheckForm(forms.SelfHandlingForm):
    name = forms.RegexField(label=_("Name"),
                            max_length=255,
                            regex=r'^[\w\.\- ]+$',
                            error_messages={'invalid': _('Name may only '
                                'contain letters, numbers, underscores, '
                                'periods and hyphens.')})

    desc = forms.CharField(label=_("Description"))
    timeout = forms.IntegerField(label=_("Timeout"), min_value=1)
    spacing = forms.IntegerField(label=_("Spacing"), min_value=1)
    code = forms.FileField(label=_("Check Code"))

    class Meta:
        name = _("Check Info")
        help_text = _("From here you can add a new check.")
        
    def format_status_message(self, message):
        return "Check %s was successfully added." % self.context['name']        

    def clean(self):
        cleaned_data = super(AddCheckForm, self).clean()
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

    def handle(self, request, data):
        # Add new check
        # check_id = data.get('check_id') or 'auto'
        try:
            code_file = request.FILES['code']
            self.object = api.nova.periodic_check_create(request,
                                                    name=data['name'],
                                                    desc=data['desc'],
                                                    timeout=data['timeout'],
                                                    spacing=data['spacing'],
                                                    code=base64.b64encode(code_file.read()))
        except Exception:
            exceptions.handle(request, _('Unable to add new check.'))
            return False

        return True


# class UpdateImageForm(forms.SelfHandlingForm):
#     image_id = forms.CharField(widget=forms.HiddenInput())
#     name = forms.CharField(max_length="255", label=_("Name"))
#     description = forms.CharField(widget=forms.widgets.Textarea(),
#                                   label=_("Description"),
#                                   required=False)
#     kernel = forms.CharField(max_length="36", label=_("Kernel ID"),
#                              required=False,
#                              widget=forms.TextInput(
#                                  attrs={'readonly': 'readonly'}
#                              ))
#     ramdisk = forms.CharField(max_length="36", label=_("Ramdisk ID"),
#                               required=False,
#                               widget=forms.TextInput(
#                                   attrs={'readonly': 'readonly'}
#                               ))
#     architecture = forms.CharField(label=_("Architecture"), required=False,
#                                    widget=forms.TextInput(
#                                        attrs={'readonly': 'readonly'}
#                                    ))
#     disk_format = forms.CharField(label=_("Format"),
#                                   widget=forms.TextInput(
#                                       attrs={'readonly': 'readonly'}
#                                   ))
#     public = forms.BooleanField(label=_("Public"), required=False)
#     protected = forms.BooleanField(label=_("Protected"), required=False)
# 
#     def __init__(self, request, *args, **kwargs):
#         super(UpdateImageForm, self).__init__(request, *args, **kwargs)
#         if not policy.check((("image", "publicize_image"),), request):
#             self.fields['public'].widget = forms.CheckboxInput(
#                 attrs={'readonly': 'readonly'})
# 
#     def handle(self, request, data):
#         image_id = data['image_id']
#         error_updating = _('Unable to update image "%s".')
# 
#         if data['disk_format'] in ['aki', 'ari', 'ami']:
#             container_format = data['disk_format']
#         else:
#             container_format = 'bare'
# 
#         meta = {'is_public': data['public'],
#                 'protected': data['protected'],
#                 'disk_format': data['disk_format'],
#                 'container_format': container_format,
#                 'name': data['name'],
#                 'properties': {'description': data['description']}}
#         if data['kernel']:
#             meta['properties']['kernel_id'] = data['kernel']
#         if data['ramdisk']:
#             meta['properties']['ramdisk_id'] = data['ramdisk']
#         if data['architecture']:
#             meta['properties']['architecture'] = data['architecture']
#         # Ensure we do not delete properties that have already been
#         # set on an image.
#         meta['purge_props'] = False
# 
#         try:
#             image = api.glance.image_update(request, image_id, **meta)
#             messages.success(request, _('Image was successfully updated.'))
#             return image
#         except Exception:
#             exceptions.handle(request, error_updating % image_id)
