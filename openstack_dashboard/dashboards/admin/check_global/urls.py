from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from openstack_dashboard.dashboards.admin.check_global import views


urlpatterns = patterns('openstack_dashboard.dashboards.admin.check_global.views',
    url(r'^$', views.IndexView.as_view(), name='index'))
