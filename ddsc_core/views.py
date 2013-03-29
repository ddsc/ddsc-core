# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import division

import ast

from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

import networkx as nx

from lizard_security.models import DataSet

from ddsc_core.models import LogicalGroup
from ddsc_core.models import LogicalGroupEdge
from ddsc_core.models import Timeseries
from ddsc_core.models import TimeseriesSelectionRule


def timeseries_from_rules(rules):
    """Return a list of timeseries based on selection rules.

    Rules are expected to be ordered by entry order (see
    class Meta of the TimeseriesSelectionRule model).
    The first rule should not have an operator.

    """

    for rule in rules:
        k, v = rule.criterion.split("=", 1)
        v = ast.literal_eval(v)
        if rule.operator is None:
            q = Q(**{k: v})
        elif rule.operator == "&":
            q = q & Q(**{k: v})
        elif rule.operator == "|":
            q = q | Q(**{k: v})

    if rules:
        return Timeseries.objects.filter(q).only("name")
    else:
        return []


class LogicalGroupGraph(View):
    """View of the graph of LogicalGroups."""

    def get(self, request, *args, **kwargs):
        """Return the graph as a png image."""
        current = LogicalGroup.objects.get(pk=kwargs['pk'])
        G = nx.DiGraph()  # NetworkX directed graph
        G.add_nodes_from(LogicalGroup.objects.all())
        G.add_edges_from(LogicalGroupEdge.edges())
        A = nx.to_agraph(G)  # Graphviz agraph
        A.graph_attr.update(rankdir="BT")
        A.node_attr.update(fontsize=9)
        A.get_node(current).attr['color'] = "red"
        A.layout(prog="dot")
        return HttpResponse(A.draw(format="png"), mimetype="image/png")


class LogicalGroupRulesView(View):
    """Expand the logical group with all timeseries that meet the rules."""

    # TODO: use more fine-grained permissions (allow owners to POST too).
    @method_decorator(permission_required('is_superuser'))
    def dispatch(self, *args, **kwargs):
        """Allow only superusers to POST."""
        return super(LogicalGroupRulesView, self).dispatch(*args, **kwargs)

    @transaction.commit_on_success
    def post(self, request, *args, **kwargs):
        logical_group = LogicalGroup.objects.get(**kwargs)  # pass pk
        content_type = ContentType.objects.get_for_model(logical_group)
        rules = TimeseriesSelectionRule.objects.filter(
            content_type_id=content_type.pk,
            object_id=logical_group.pk
        )
        logical_group.timeseries.add(*timeseries_from_rules(rules))
        return HttpResponse()


class DataSetRulesView(View):
    """Expand the data set with all timeseries that meet the rules."""

    # TODO: use more fine-grained permissions (allow owners to POST too).
    @method_decorator(permission_required('is_superuser'))
    def dispatch(self, *args, **kwargs):
        """Allow only superusers to POST."""
        return super(DataSetRulesView, self).dispatch(*args, **kwargs)

    @transaction.commit_on_success
    def post(self, request, *args, **kwargs):
        data_set = DataSet.objects.get(**kwargs)  # pass pk
        content_type = ContentType.objects.get_for_model(data_set)
        rules = TimeseriesSelectionRule.objects.filter(
            content_type_id=content_type.pk,
            object_id=data_set.pk
        )
        data_set.timeseries.add(*timeseries_from_rules(rules))
        return HttpResponse()
