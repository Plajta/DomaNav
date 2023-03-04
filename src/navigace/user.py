import numpy as np
import math

class user:

    def __init__(self, x, y, ang) -> None:
        self.x=x
        self.y=y
        self.ang=ang
        pass
    def get_angle(self,last_x,last_y):
        return  np.rad2deg(math.atan2((last_x-self.x),(last_y-self.y)))

    def update(self,new_x,new_y):
        self.old_x=self.x
        self.x=new_x
        self.old_y=self.y
        self.y=new_y
        self.ang=self.get_angle(self.old_x,self.old_y)
        

test=user(0,0,0)
test.get_angle(math.sqrt(3),1)
print(test.ang)
    