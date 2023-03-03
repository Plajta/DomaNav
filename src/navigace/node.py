class node:
    x=0.0 
    y=0.0
    paths = {
        'a': ['b', 'c'],
        'b': ['a'],
        'c': ['d', 'f'],
        'd': ['c', 'e'],
        'e': ['d'],
        'f': ['c']}