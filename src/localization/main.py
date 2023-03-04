import serial

class localizator:
    def __init__ (self):
        self.port = ""
        with open('port.conf', encoding="utf-8") as f:
            self.port = f.read()
            print(self.port)
        ser = serial.Serial(self.port, 115200, timeout=3)
        ser.write(b'r')
        ser.close()

    def scan (self,cmd='u'):
        scan_output = ""
        ser = serial.Serial(self.port, 115200, timeout=3)
        ser.write(cmd.encode("ASCII"))
        while True:
            znak = ser.read()
            if znak != b'\x00':
                scan_output = scan_output + str(znak.decode("ASCII"))
            else:
                print(scan_output.count('\n'))
                ser.close()
                break
        ser.close()
        return scan_output



if __name__ == "__main__":
    mapa = "";
    locate = localizator()
    for i in range(2):
        input("Stiskni enter pro načtení " + str(i) + " mapy")
        aktualni = locate.scan('m')
        print (aktualni)
        mapa = mapa + aktualni
    #print(locate.scan())
    with open('wifi.map', 'w', encoding="utf-8") as f:
        f.write(mapa)
