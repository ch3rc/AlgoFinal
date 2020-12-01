"""
Author:         Cody Hawkins
Date:           12/1/2020
Class:          5130
File:           display_nodes.py
Desc:           Graph class that takes in edges and provides
                a shortest path of the origin to destination.
                If all nodes were shown it would be unreadable,
                this cuts the graph down to the relevant path
"""
import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    """To be used with wiki crawler to display nodes"""
    def __init__(self, origin, keyword):
        self.origin = origin
        self.keyword = keyword
        self.G = nx.Graph()
        self.DG = nx.DiGraph()
        self.color = []
        self.size = []

    def add_edges(self, parent, child):
        self.G.add_edge(parent, child)

    def change_node_colors(self):
        for node in self.DG:
            self.size.append(2000)
            if node == self.keyword:
                # keyword set to green
                self.color.append("#2ee809")
            elif node == self.origin:
                # start word set to light blue
                self.color.append("#07eef2")
            else:
                # non start word or keyword set to red
                self.color.append("#e81809")

    def shortest_path(self):
        origin_node = self.origin
        graph = self.G
        # get all shortest paths of start node
        paths = nx.single_source_shortest_path(graph, origin_node)
        dest = self.keyword
        # get path from origin to destination
        destination = paths[dest]

        nodes = []
        # create edges for origin to destination
        for i, edges in enumerate(destination):
            if i > 0:
                nodes.append((destination[i - 1], destination[i]))
        # add the new path to a directed graph and display
        self.DG.add_edges_from(nodes)
        self.change_node_colors()

    def show_graph(self):
        self.shortest_path()
        nx.draw(self.DG, alpha=0.8, with_labels=True, font_weight='bold', node_color=self.color, node_size=self.size)
        plt.show()