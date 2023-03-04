import numpy as np
import math
from node import node
from graf import Graph
nodes = {
'a': node(['b','c'], 10, 7,"a"),
'b': node(["a"], 10, 14.2,"b"),
'c': node(['a','d', 'f'], 15.8, 7,"c"),
'd': node(['c', 'e'], 15.8, 14.2,"d"),
'e': node(['d'], 19.4, 14.2,"e"),
'f': node(['c'], 19.4, 7,"f")
}
class user:
    toleration=1
    def __init__(self, x, y, ang, graf, last_point) -> None:
        self.x = x
        self.y = y
        self.ang = ang
        self.last_point = last_point
        self.graf=graf
        
        pass

    def get_angle(self, last_x, last_y):
        #gets the angle of the person from two last known coordinates
        self.ang = np.rad2deg(math.atan2((last_x-self.x),(last_y-self.y)))
        
    def get_node_angle(self):
        self.node_ang = np.rad2deg(math.atan2((self.x - self.next_point.x),(self.y - self.next_point.y))) - self.ang

    def update(self, new_x, new_y):
        #updates coordinates of the person
        self.old_x = self.x
        self.x = new_x
        self.old_y = self.y
        self.y = new_y
        self.get_angle(self.old_x, self.old_y)
        for point_index in self.last_point.neighbours:
            point=self.graf._graph[point_index]
            print(point_index+": "+ str(math.sqrt(math.pow(point.x-self.x,2)+math.pow(point.y-self.y,2))))
            if math.sqrt(math.pow(point.x-self.x,2)+math.pow(point.y-self.y,2))<self.toleration:
                self.last_point=point
                self.set_dest("e")
                break
        self.check_angle()

    def set_dest(self,target):
        if(self.last_point.name!=target):
            self.next_point = self.graf.shortest_path(self.last_point.name, target)[1]

    def check_angle(self):
        if (self.get):
        if (self.node_ang>=45):
            print("Jdi vlevo")
        
        if (self.get_angle(self.old_x, self.old_y) <=-45 and self.get_angle(self.old_x, self.old_y) >= -135):
            print("Jdi vpravo")
        
    
u= user(10,7,0,Graph(nodes),nodes['a'])
while (u.last_point.name!="e"):
    u.update(float(input("x: ")),float(input("y: ")))

#print(u.next_point)
    