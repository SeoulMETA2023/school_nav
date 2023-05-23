from script.util import get_distance


class Map:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[int(node)] = node
        return self

    def get_cost(self, start, end):
        return get_distance(self.nodes[start].pos, self.nodes[end].pos)

    def __iter__(self):
        return iter(self.nodes.values())

    def __getitem__(self, num):
        return self.nodes[num]


class Node:
    def __init__(self, num, pos, linked):
        self.num = num
        self.pos = pos
        self.linked = linked

    def __iter__(self):
        return iter(self.linked)

    def __int__(self):
        return self.num

    def __str__(self):
        return str(self.num)
