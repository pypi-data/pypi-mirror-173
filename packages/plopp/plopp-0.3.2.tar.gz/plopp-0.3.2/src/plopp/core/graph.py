# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Scipp contributors (https://github.com/scipp)

from html import escape


def _make_graphviz_digraph(*args, **kwargs):
    try:
        from graphviz import Digraph
    except ImportError:
        raise RuntimeError(
            "Failed to import `graphviz`. "
            "Use `pip install graphviz` (requires installed `graphviz` executable) or "
            "`conda install -c conda-forge python-graphviz`.")
    return Digraph(*args, **kwargs)


def _add_graph_edges(dot, node, inventory, hide_views):
    label = escape(str(
        node.func)) + '\nid = ' + node.id if node.name is None else escape(node.name)
    inventory.append(node.id)
    dot.node(node.id, label=label)
    for child in node.children:
        key = child.id
        if key not in inventory:
            dot.edge(node.id, key)
            _add_graph_edges(dot, child, inventory, hide_views)
    for parent in node.parents + list(node.kwparents.values()):
        key = parent.id
        if key not in inventory:
            dot.edge(key, node.id)
            _add_graph_edges(dot, parent, inventory, hide_views)
    if not hide_views:
        for view in node.views:
            key = view.id
            dot.node(key,
                     label=view.__class__.__name__,
                     shape='ellipse',
                     style='filled',
                     color='lightgrey')
            dot.edge(node.id, key)


def show_graph(node, size=None, hide_views=False):
    dot = _make_graphviz_digraph(strict=True)
    dot.attr('node', shape='box', height='0.1')
    dot.attr(size=size)
    inventory = []
    _add_graph_edges(dot, node, inventory, hide_views)
    return dot
