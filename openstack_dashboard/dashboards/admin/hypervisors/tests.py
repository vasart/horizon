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

from django.core.urlresolvers import reverse
from django import http
from mox import IsA  # noqa

from openstack_dashboard import api
from openstack_dashboard.test import helpers as test


class HypervisorViewTest(test.BaseAdminViewTests):
    @test.create_stubs({api.nova: ('hypervisor_list',
                                   'hypervisor_stats')})
    def test_index(self):
        hypervisors = self.hypervisors.list()
        stats = self.hypervisors.stats
        api.nova.hypervisor_list(IsA(http.HttpRequest)).AndReturn(hypervisors)
        api.nova.hypervisor_stats(IsA(http.HttpRequest)).AndReturn(stats)
        self.mox.ReplayAll()

        res = self.client.get(reverse('horizon:admin:hypervisors:index'))
        self.assertTemplateUsed(res, 'admin/hypervisors/index.html')
        self.assertItemsEqual(res.context['table'].data, hypervisors)


class HypervisorDetailViewTest(test.BaseAdminViewTests):
    @test.create_stubs({api.nova: ('hypervisor_search',)})
    def test_index(self):
        hypervisor = self.hypervisors.list().pop().hypervisor_hostname
        api.nova.hypervisor_search(
            IsA(http.HttpRequest), hypervisor).AndReturn([])
        self.mox.ReplayAll()

        url = reverse('horizon:admin:hypervisors:detail', args=[hypervisor])
        res = self.client.get(url)
        self.assertTemplateUsed(res, 'admin/hypervisors/detail.html')
        self.assertItemsEqual(res.context['table'].data, [])
