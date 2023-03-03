from node import node

class graf:

    nodes = {
    'a': node(['b'],"a"),
    'b': ['a'],
    'c': ['d', 'f'],
    'd': ['c', 'e'],
    'e': ['d'],
    'f': ['c']}
