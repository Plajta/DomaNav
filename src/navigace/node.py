class node:
    x=0.0 
    y=0.0
    neighbours=[]
    used=False
    name=""
    def __init__(self, n, x, y,name) -> None:

        self.neighbours = n
        self.x = y
        self.y = x
        self.name = name
        pass