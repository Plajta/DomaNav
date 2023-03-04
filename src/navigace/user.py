import numpy as np
import math
from node import node
from graf import Graph
from serial import Serial
import threading

nodes = {
'a': node(['b','c'], 10, 7,"a"),
'b': node(["a"], 10, 14.2,"b"),
'c': node(['a','d', 'f'], 15.8, 7,"c"),
'd': node(['c', 'e'], 15.8, 14.2,"d"),
'e': node(['d'], 19.4, 14.2,"e"),
'f': node(['c'], 19.4, 7,"f")
}



Prvni_NP = {
'predsin': node(['garaz','obyv_p1'], 6, 5.7,"predsin"),
'garaz': node(["predsin"], 6, 2.4,"garaz"),
'obyv_p1': node(['predsin','obyv_p2', 'schody'], 9.5, 5.7,"obyv_p1"),
'obyv_p2': node(['obyv_p1', 'obyv_p3', 'kk'], 12.8, 5.7,"obyv_p2"),
'obyv_p3': node(['obyv_p2'], 12.8, 8,"obyv_p3"),
'kk': node(['obyv_p2'], 14.2, 2.4,"kk")
}

Druhe_NP = {
'schody': node(['podkrov_1','pracovna'], 7.1, 3.5,"schody"),
'podkrov_1': node(['schody','podkrov_2'], 10, 3.5,"podkrov_1"),
'pracovna': node(['schody'], 4.6, 3.5,"pracovna"),
'podkrov_2': node(['koupelna', 'podkrov_3'], 10, 4.7,"podkrov_2"),
'koupelna': node(['podkrov_2'], 7.1, 4.7,"koupelna"),
'podkrov_3': node(['loznice', 'dets_pok'], 11.6, 4.7,"podkrov_3"),
'loznice': node(['podkrov_3'], 11.6, 9.9,"loznice"),
'dets_pok': node(['podkrov_3'], 15, 4.7,"dets_pok")
}

class user:
    toleration=1
    next_point=None
    node_ang=0
    def __init__(self, x, y, ang, graf, target) -> None:
        self.serial_read()
        self.x = x
        self.y = y
        self.ang = ang
        point = node([],0,0,"")
        for nodid in nodes:
            
            nod=nodes[nodid]
            if point.name=="" or (math.sqrt(math.pow(point.x-self.x,2)+math.pow(point.y-self.y,2)))>((math.sqrt(math.pow(nod.x-self.x,2)+math.pow(nod.y-self.y,2)))):
                point=nod
        print(point.name)
        self.last_point = point
        self.graf=graf
        self.target=target
        self.update(x,y)
        pass

    def get_angle(self, last_x, last_y):
        #gets the angle of the person from two last known coordinates
        self.ang = np.rad2deg(math.atan2((last_x-self.x),(last_y-self.y)))
        
    def get_node_angle(self):
        self.node_ang = np.rad2deg(math.atan2((self.x - self.next_point.x),(self.y - self.next_point.y))) - self.ang

    def update(self, new_x, new_y):
        #updates coordinates of the person
        self.serial_read()
        self.old_x = self.x
        self.x = new_x
        self.old_y = self.y
        self.y = new_y
        self.get_angle(self.old_x, self.old_y)
        print(self.ang)
        
        for point_index in self.last_point.neighbours:
            point=self.graf._graph[point_index]
            print(point_index+": "+ str(math.sqrt(math.pow(point.x-self.x,2)+math.pow(point.y-self.y,2))))
            if math.sqrt(math.pow(point.x-self.x,2)+math.pow(point.y-self.y,2))<self.toleration:
                self.last_point=point
                self.set_dest(self.target)
                break
        if(self.next_point==None):
            self.set_dest(self.target)
        self.get_node_angle()
        self.check_angle()

    def set_dest(self,target):
        if(self.last_point.name!=target):
            #print(self.graf.shortest_path(self.last_point.name, target))
            self.next_point =nodes[self.graf.shortest_path(self.last_point.name, target)[1]]

    def check_angle(self): 
        #silena matematika tvori uhly
        differ=self.node_ang
        if (abs(differ)>180):
            differ_final=360-abs(differ)
            if(differ>0):
                differ_final*=-1
        else:
            differ_final=differ

        if (abs(differ_final) > 120):
            print("Otoc se a jdi k:"+self.next_point.name)
        elif (differ_final > 30):
            print("Jdi vpravo směrem k:"+self.next_point.name)       
        elif (differ_final < -30 ):
            print("Jdi vlevo směrem k:"+self.next_point.name)
        print(self.node_ang)
        print(self.ang)
        print(differ_final)

    
    def serial_read(self):
        serial = Serial()
        serial.baudrate = 115200
        serial.port = "COM7"
        serial.open()
        data = serial.readline().decode("ASCII")
        print(f"{data} °")


    
    def start_thread_readSerial(self):
        # creating thread
        t1 = threading.Thread(target=self.serial_read,args=10)
        # starting thread 1
        t1.start()

        
nodes=Prvni_NP
u= user(6,5.7,0,Graph(nodes),"kk")
while (u.last_point.name!="kk"):
    u.update(float(input("x: ")),float(input("y: ")))
    

#print(u.next_point)
    