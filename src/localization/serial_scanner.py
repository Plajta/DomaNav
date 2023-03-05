import serial

class scanner:
    def __init__ (self,port="/dev/ttyUSB0"):
        self.port = port
        ser = serial.Serial(self.port, 115200, timeout=3)
        ser.write(b'r')
        self.type = self.get_type()
        ser.close()

    def scan (self):
        scan_output = ""
        ser = serial.Serial(self.port, 115200, timeout=3)
        ser.write(b'u')
        while True:
            znak = ser.read()
            #print(znak)
            if znak != b'@':
                scan_output = scan_output + str(znak.decode("ASCII"))
            else:
                #print(scan_output.count('\n'))
                ser.close()
                break
        ser.close()
        return scan_output[:-1]

    def get_type (self):
        type = ""
        ser = serial.Serial(self.port, 115200, timeout=3)
        ser.write(b'p')
        while True:
            znak = ser.read()
            #print(znak)
            if znak != b'@':
                type = type + str(znak.decode("ASCII"))
            else:
                #print(scan_output.count('\n'))
                ser.close()
                break
        ser.close()
        return type



if __name__ == "__main__": # When run as a standalone module it tries to produce a map
    mapa = ""
    port = ""
    with open('port.conf', encoding="utf-8") as f:
        port = f.read()
    print(port)
    locate = scanner(port)
    for i in range(20   ): #tady se zvyšuje množství zón
        input("Stiskni enter pro načtení " + str(i) + " mapy")
        aktualni = f"oblast;{str(i+1)}\n"
        aktualni = aktualni + locate.scan() + '\n'
        print(aktualni)
        mapa = mapa + aktualni
    #print(locate.scan())
    mapa = mapa[:-1]
    with open('wifi.map', 'w', encoding="utf-8") as f:
        f.write(mapa)
