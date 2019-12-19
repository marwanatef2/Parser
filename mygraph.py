from graphviz import Digraph

import os
os.environ["PATH"] += os.pathsep + \
    'D:\Marwan\projects\Parser\graphviz-2.38\\release\\bin'

dot = Digraph(comment='The Round Table')

class Node:
    def __init__(self, name, text, shape='oval'):
        self.name = name
        self.text = text
        self.shape = shape

    def addNode(self):
        dot.node(self.name, self.text, shape=self.shape)

    def addChild(self, child):
        dot.edge(self.name, child.name)
