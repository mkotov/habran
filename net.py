#!/usr/bin/env python

import networkx as nx
import matplotlib.pyplot as plt
import math

MAX_NUM_OF_LABELS = 25

def read_data(file_name):
    G = nx.DiGraph()
    karmas = {}
    with open(file_name, "r") as input_file:
        for line in input_file.readlines()[1:]:
            name, karma, country, region, city, first_date, last_date, invited_by, invited = line.split(";")
            name = name.strip()
            karma = karma.strip()
            invited_by = invited_by.strip()
            invited = invited.strip()
            if invited:
                invited = [i.strip() for i in invited.split(",")]
            else:
                invited = []
            G.add_node(name)
            if invited_by:
                G.add_edge(invited_by, name)
            for i in invited:
                G.add_edge(name, i)
            karmas[name] = karma
    return G, karmas


def draw(G, karmas):
    def get_root(G):
        for x in G.nodes():
            if len(G.predecessors(x)) == 0:
                return x
        return None
    
    def gen_node_size(karma):
        if karma == "RO" or karma == "DA":
            return 1
        else:
            return max(1, math.sqrt(abs(float(karma))))
    
    def gen_node_sizes(karmas, nodes):
        return [20 * gen_node_size(karmas[n]) for n in nodes]
    
    def gen_node_color(karma):
        if karma == "RO":
            return "darkgray"
        elif karma == "DA":
            return "darkgray"
        elif float(karma) > 0:
            return "green"
        elif float(karma) < 0:
            return "red"
        else:
            return "blue"
    
    def gen_node_colors(karmas, nodes):
        return [gen_node_color(karmas[n]) for n in nodes]
    
    def gen_node_labels(karmas, G):
        ranks = []
        root = get_root(G)
        for n in G.nodes():
            r = len(G.successors(n)) * 10
            if karmas[n] != "RO" and karmas[n] != "DA":
             r += abs(float(karmas[n]))
            if n == root:
                r += 1000
            ranks.append([n, r])
        return dict((p[0], p[0]) for p in sorted(ranks, key=lambda p: p[1], reverse=True)[0:MAX_NUM_OF_LABELS])

    nx.draw(G, 
            nx.graphviz_layout(G, prog="neato", root=get_root(G)), 
            node_size=gen_node_sizes(karmas, G.nodes()), 
            node_color=gen_node_colors(karmas, G.nodes()), 
            arrows=True, 
            labels=gen_node_labels(karmas, G), 
            with_labels=True, 
            font_size="10", 
            edge_color="lightgrey", 
            linewidths=0)

def get_karma(karmas, n):
    if karmas[n] == "RO" or karmas[n] == "DA":
        return 0
    else:
        return float(karmas[n])

def main():
    G, karmas = read_data("karma.txt")
    cs = nx.weakly_connected_component_subgraphs(G)
    cs.sort(key=lambda c: c.number_of_nodes(), reverse=True)

    plt.clf()
    draw(cs[126], karmas)
    plt.show()

if __name__ == "__main__":
    main()
