# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import division

from django.http import HttpResponse
from django.views.generic import View
import networkx as nx

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
