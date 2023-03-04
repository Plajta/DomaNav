from serial_scanner import scanner
from array import array

class finder:
    def __init__(self,map="wifi.map"):
        with open(map, encoding="utf-8") as f:
            self.map = f.read()
        with open('port.conf', encoding="utf-8") as f:
            self.port = f.read()
        self.map = self.map.split('\n')
        self.decoded_map = list()
        oblast_list = list()
        for line in self.map:
            line = line.split(';')
            if line[0] != "oblast":
                oblast_list.append(line)
            else:
                self.decoded_map.append(oblast_list)
                oblast_list.clear()


    def find(self):
        loc = scanner(self.port)
        scan = loc.scan()
        out = [step.split(';') for step in scan.split('\n')]
        zone_counter = 0
        score = [0] * len(self.decoded_map)
        for i,zone in enumerate(self.decoded_map):
            for bssid_in_zone in zone:
                for bssid in out:
                    if(bssid[0]==bssid_in_zone[0]):
                        print(str(bssid[0]) + ", Zóna: " + str(i))
                        score[i]+=1
        print(score)
        
if __name__ == "__main__": # When run as a standalone module it tries to find you
    Finder = finder()
    Finder.find()