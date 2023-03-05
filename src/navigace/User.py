import numpy as np
import math
from navigace.Node import node
from navigace.graf import Graph
from navigace import controlAccel
from serial import Serial
import serial
import serial.tools.list_ports as list_ports

Prvni_NP = {
'predsin': node(['garaz','obyv_p1'], 6, 5.7,"predsin"),
'garaz': node(["predsin"], 6,2.4,"garaz"),
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
Subnotes={
"postel_zdeněk":node(["obyv_p3"],16.5,10.5,"postel_zdeněk"),
"židle_zdeněk":node(["obyv_p2"],14.2,5.9,"židle_zdeněk"),
"zachod":node(["predsin"],6.3,8,"zachod"),
"křeslo_u_TV":node(["obyv_p3"],14.2,9.5,"křeslo_u_TV"),
"lednice":node(["kk"],16.5,0.5,"lednice"),
"jidelni_stul":node(["obyv_p2"],15.8,7,"jidelni_stul"),
"rohova_sedačka":node(["obyv_p3"],10.5,8.6,"rohova_sedačka"),
"krbová_kamna":node(["obyv_p3"],9.5,12.3,"krbová_kamna"),
"konferenční_stolek":node(["obyv_p3"],11,10,"konferenční_stolek"),
"křeslo":node(["obyv_p2"],12,4.2,"křeslo"),
"televize":node(["obyv_p3"],12,12.3,"televize")
}
"""
#Bude použito na prezentaci
TestPrezentace = { #x, y notation (s21 - xy)
    "s21": [[2, 1], [1, 1]],
    "s11": [[1, 1], [1, 2]],
    "s12": [[1, 2], [1, 3]],
    "s13": [[1, 3], [1, 4]] #notace: prakticky linked list s nodami jako sektory
}
"""

nodes = None #setup in main

class user:
    toleration=1
    next_point=None
    node_ang=0
    def __init__(self, x, y, ang, graf, target="") -> None:
        
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
        self.target=""
        self.target=target
        self.update(x,y)
        pass

    def get_angle(self):
        #gets the angle from compass
        read = self.serial_read()
        if read:
            self.ang = read
        
    def get_node_angle(self):
        #tg^-1 (x1-x2)/(y1-y2) 
        self.node_ang = np.rad2deg(math.atan2((self.y - self.next_point.y),(self.x - self.next_point.x))) - self.ang

    def update(self, new_x, new_y):
        #updates coordinates of the person
        self.old_x = self.x
        self.x = new_x
        self.old_y = self.y
        self.y = new_y
        self.get_angle()
        print(f"self angle = {self.ang}")
        
        print(self.last_point.neighbours)
        for point_index in [self.last_point.neighbours]:
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



    def set_dest(self,target=""):
        if(self.last_point.name!=Subnotes[target].neighbours[0]):
            #set destination
            
            self.next_point = nodes[self.graf.shortest_path(self.last_point.name, Subnotes[target].neighbours[0])[1]]
        else:
            self.next_point=Subnotes[target]


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
            print("Otoc se a jdi k:" + self.next_point.name)
            return 1
        elif (differ_final > 30):
            print("Jdi vpravo směrem k:" + self.next_point.name)   
            return 2    
        elif (differ_final < -30 ):
            print("Jdi vlevo směrem k:" + self.next_point.name)
            return 3
        else:
            return 4
        #
        print(self.node_ang)
        print("differ final " + str(differ_final))


    def serial_read(self):
        serial = controlAccel.find_comport(controlAccel.PID_MICROBIT, 
                                  controlAccel.VID_MICROBIT, 115200)

        serial.open()
        data = serial.readline().decode("utf-8")
        if data:
            data = int(data.rstrip("\n"))
            print(f"data1 = {data}")
            data = -1*(180-(data-180))
            #pretekajici uhly jsou sračka
            if(data<-180):
                data+=360
            elif(data>180):
                data-=360
            
            print(f"data2 = {data}")
            return data
        return None



    def load_nodes(self,name):
        nodes={}
        f = open(name)
        lines = f.readlines()
        f.close
        for line in lines:
            parts=line.split(";")
            node_name=parts[0]
            node_x=float(parts[1])
            node_y=float(parts[2])
            remains=[]
            if(parts.__len__>3):
                for num in range(3,parts.__len__):
                    remains.append(parts[num])
            self.nodes.update({node_name:node(remains,node_x,node_y,node_name)})

""" TODO
u= user(6,7,0,Graph(nodes),"zachod")
while (u.last_point.name!="zachod"):
    u.update(float(input("x: ")),float(input("y: ")))
"""