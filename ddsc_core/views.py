# (c) Nelen & Schuurmans. MIT licensed, see LICENSE.rst.

from __future__ import division

from django.http import HttpResponse
from django.views.generic import View
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

from ddsc_core.models import LogicalGroup
from ddsc_core.models import LogicalGroupEdge


class LogicalGroupGraph(View):
    """View of the graph of LogicalGroups."""

    def get(self, request, *args, **kwargs):
        """Return the graph as a png image."""
        G = nx.DiGraph()
        G.add_nodes_from(LogicalGroup.objects.all())
        G.add_edges_from(LogicalGroupEdge.edges())
        #logical_group = LogicalGroup.objects.get(pk=kwargs['pk'])
        nx.draw_networkx(G, pos=nx.graphviz_layout(G))
        response = HttpResponse(content_type="image/png")
        plt.axis('off')
        plt.savefig(response, format="png")
        plt.close()
        return response
