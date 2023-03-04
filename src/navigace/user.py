import numpy as np
import math
from node import node
from graf import Graph
nodes = {
'a': node(['b'], 10, 7,"a"),
'b': node(["a"], 10, 14.2,"b"),
'c': node(['d', 'f'], 15.8, 7,"c"),
'd': node(['c', 'e'], 15.8, 14.2,"d"),
'e': node(['d'], 19.4, 14.2,"e"),
'f': node(['c'], 19.4, 7,"f")
}
class user:
    toleration=0.005
    def __init__(self, x, y, ang, graf, last_point) -> None:
        self.x = x
        self.y = y
        self.ang = ang
        self.last_point = last_point
        self.graf=graf
        
        pass

    def get_angle(self, last_x, last_y):
        #gets the angle of the person from two last known coordinates
        return  np.rad2deg(math.atan2((last_x-self.x),(last_y-self.y)))
        

    def update(self, new_x, new_y):
        #updates coordinates of the person
        self.old_x = self.x
        self.x = new_x
        self.old_y = self.y
        self.y = new_y
        self.ang = self.get_angle(self.old_x, self.old_y)
        for point_index in self.last_point.neighbours:
            point=self.graf._graph[point_index]
            print( math.sqrt(math.pow(point.x-self.x,2)+math.pow(point.y-self.y,2)))
            if math.sqrt(math.pow(point.x-self.x,2)+math.pow(point.y-self.y,2))<self.toleration:
                self.last_point=point
                self.set_path(input())
                break
    
    def set_path(self,target):
        if(self.last_point.name!=target):
            self.next_point = self.graf.shortest_path(self.last_point.name, target)[1]



        
    
u= user(15.8,14.2,0,Graph(nodes),nodes['c'])
u.update(15.8,14.2)
print(u.next_point)
    