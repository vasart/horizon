from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from .views import IndexView

from openstack_dashboard.dashboards.admin.check_config import views


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^add/$', views.AddView.as_view(), name='add'),
    url(r'^(?P<id>[^/]+)/update/$', views.UpdateView.as_view(), name='update'),
    # url(r'^(?P<id>[^/]+)/details/', views.DetailsView.ad_view(), name='details'),
)
