class node:
    x=0.0 
    y=0.0
    neighbours=[]
    used=False
    name=""
    def __init__(self, n, x, y,name="") -> None:

        self.neighbours = n
        self.x = x
        self.y = y
        self.name = name
        pass