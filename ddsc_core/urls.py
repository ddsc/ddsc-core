# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from django.conf.urls import include, patterns, url
from django.contrib import admin

from ddsc_core.views import LogicalGroupGraph
from ddsc_core.views import SelectionRulesView

admin.autodiscover()

urlpatterns = patterns('',
    url(
        r'^logical_groups/(?P<pk>\d+)/graph/$',
        LogicalGroupGraph.as_view(),
        name='logical_group_graph'
    ),
    url(
        r'^admin/ddsc_core/logicalgroup/(?P<pk>\d+)/rules/$',
        SelectionRulesView.as_view(),
    ),
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
)
