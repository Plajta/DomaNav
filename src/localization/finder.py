from serial_scanner import scanner
from array import array

class finder:
    def __init__(self,map="wifi.map"):
        with open(map, encoding="utf-8") as f:
            self.map = f.read()
        with open('port.conf', encoding="utf-8") as f:
            self.port = f.read()
        self.map = self.map.split('\n')
        self.decoded_map = []
        oblast_list = []
        for line in self.map:
            line = line.split(';')
            if line[0] != "oblast":
                oblast_list.append(line)
            else:
                if line[1] != str(1):
                    self.decoded_map.append(oblast_list.copy())
                    oblast_list.clear() #this is fricking disgusting


    def find(self):
        loc = scanner(self.port)
        scan = loc.scan()
        out = [step.split(';') for step in scan.split('\n')]
        score = [0]*len(self.decoded_map)
        
        for i,zone in enumerate(self.decoded_map):
            for bssid_in_zone in zone:
                for bssid in out:
                    if(bssid[0]==bssid_in_zone[0]):
                        #print(str(bssid[0])+ ", Síla: " + str(bssid_in_zone[1]) + ", Zóna: " + str(i))
                        score[i]-=abs(int(bssid[1])-int(bssid_in_zone[1]))
        
        score_sorted = score.copy()
        score_sorted.sort(reverse=True)
        rating = score_sorted[0]

        #           position in default array, whole len of default array
        return score.index(rating), len(self.decoded_map) #just to return whole len of positions

        


if __name__ == "__main__": # When run as a standalone module it tries to find you
    Finder = finder()
    Finder.find()