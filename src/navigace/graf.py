from node import node

class graf:

    nodes = {
    'a': node(['b'],"a"),
    'b': node(["a"],"b"),
    'c': ['d', 'f'],
    'd': ['c', 'e'],
    'e': ['d'],
    'f': ['c']}
