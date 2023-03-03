from node import node

class graf:

    nodes = {
    'a': node(['b'],"a"),
    'b': node(["a"],"b"),
    'c': node(['d', 'f'],"c"),
    'd': node(['c', 'e'],"d"),
    'e': node(['d'],"e"),
    'f': node(['c'],"f")}
