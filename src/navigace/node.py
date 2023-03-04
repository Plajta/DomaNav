class node:
    
    neighbours=()
    used=False
    name=""
    def __init__(self, n, x, y) -> None:

        self.neighbours = n
        self.x = x
        self.y = y
        pass