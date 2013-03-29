# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from django.conf.urls import include, patterns, url
from django.contrib import admin

from ddsc_core.views import DataSetRulesView
from ddsc_core.views import LogicalGroupGraph
from ddsc_core.views import LogicalGroupRulesView

admin.autodiscover()

urlpatterns = patterns('',
    url(
        # For adding Timeseries to a DataSet via selection rules.
        r'^dataset/(?P<pk>\d+)/rules/$',
        DataSetRulesView.as_view(),
        name='data_set_rules'
    ),
    url(
        # For displaying the graph of LogicalGroups as an image.
        r'^logicalgroup/(?P<pk>\d+)/graph/$',
        LogicalGroupGraph.as_view(),
        name='logical_group_graph'
    ),
    url(
        # For adding Timeseries to a LogicalGroup via selection rules.
        r'^logicalgroup/(?P<pk>\d+)/rules/$',
        LogicalGroupRulesView.as_view(),
        name='logical_group_rules'
    ),
    url(
        # Handy when running ddsc_core stand-alone.
        r'^admin/',
        include(admin.site.urls)
    ),
)
