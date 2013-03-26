# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import division

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import View
import networkx as nx
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from ddsc_core.models import LogicalGroup
from ddsc_core.models import LogicalGroupEdge


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


class SelectionRulesView(View):
    """Docstring."""

    @method_decorator(permission_required('is_superuser'))
    def dispatch(self, *args, **kwargs):
        return super(SelectionRulesView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        group = LogicalGroup.objects.get(**kwargs)
        group.timeseries.add(*group.get_timeseries())
        return HttpResponseRedirect(reverse(
            'admin:ddsc_core_logicalgroup_change', args=(group.pk, )
        ))
