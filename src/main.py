#custom imports:
from SpeechRec import speech_funcs
from localization import finder
from navigace import Node, User, controlAccel, graf #TODO: i have to repair that COM3 problem
import time
import math

#
# actual code for controlling a human
#

#TODO:
#1) akcelerometr, gyroskop, atd. - done
#2) Kam jdeš? - done
#3) lokalizace - dominik + vašek
#4) graf - jéňa + karel + zapomněl jsem jméno
#5) cesta - i dunno
#6) kontrola člověka - done
#7) konec?

#
# VARIABLES
#
Command_buffer = []
last_deg = 0
d_deg = 0
Pass = False
KamJdesCount = False

Desired_Data = {
    "postel": ["postel", "posteli", "postelí", "postele"],
    "stůl": ["stůl", "stolu", "stolem"],
    "křeslo": ["křeslo", "křesla", "křeslu", "křeslem"],
    "televize": ["televize", "televizi", "televizí"],
    "záchod":  ["záchod", "záchodu", "záchodě", "záchodem"],
    "lednice": ["lednice", "lednici", "lednicí"],
    "kuchyň": ["kuchyň", "kuchyně", "kuchyní", "kuchyni"],
    "koupelna": ["koupelna", "koupelny", "koupelně", "koupelnu", "koupelnou"],
    "ložnice": ["ložnice", "ložnici", "ložnicí"]
}

TestPrezentace = {
                    "s21" : Node.node("s11", 2, 1, "s21"),
                    "s11" : Node.node("s12", 1, 1, "s11"),
                    "s12" : Node.node("s13", 1, 2, "s12"),
                    "s13" : Node.node("lednice", 1, 3, "s13") #s14 = lednice
                }

User.nodes = TestPrezentace


for i in range(0, speech_funcs.numdevices):
    if (speech_funcs.Pyaudio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", speech_funcs.Pyaudio.get_device_info_by_host_api_device_index(0, i).get('name'))


#
# MAIN
#
mapsize=5
micro_object = controlAccel.setup()
with speech_funcs.sr.Microphone() as source:
    speech_funcs.Recognizer.adjust_for_ambient_noise(source)
    f = finder.finder("../../wifi.map")
    position=[0,20]
    loc_last = [0, 0]
    while True:

        data = controlAccel.GetData(micro_object)
        if data:
            data = int(data.rstrip("\n"))
            if last_deg != 0:
                d_deg = abs(int(float(last_deg)) - int(float(data))) #literally useless to do, but always drops an error about newline
            last_deg = data
        
            print(d_deg)
            if d_deg > 1 and not KamJdesCount:
                speech_funcs.PlaySpeech("KamJdes")
                KamJdesCount = True

            time.sleep(1)
            
            Commands = speech_funcs.SpeechToText(source)
            if len(Commands) == 0: #skipping empty command
                continue
            else:
                

                Command_buffer.extend(Commands)
                print(Command_buffer)

                #nějaké vyhodnocení a nalezení místnosti
                for key in Desired_Data:
                    y_data = Desired_Data[key]
                    for data in y_data:
                        Command_buffer = [item.lower() for item in Command_buffer]
                        if data in Command_buffer: #We found desired word!
                            word = data

                            loc_last = [0, 0]
                            position=f.find()
                            if word == "lednice": #pro teď budeme používat jenom 1 class


                                TestPrezentace = {
                                    "s21" : Node.node(["s11","s13"], 3, 3, "s21"),
                                    "s11" : Node.node(["s12","s21"], 0, 3, "s11"),
                                    "s12" : Node.node(["s13"], 0, 0, "s12"),
                                    "s13" : Node.node([], 3, 0, "s13")
                                }
                                User.Subnotes={"lednice":Node.node(["s13"],3,0,"lednice")}
                                u= User.user(loc_last[0],loc_last[1],0,graf.Graph(TestPrezentace),"lednice")
                                for key in User.user.TestPrezentace:
                                    print("ano")

                                    loc_now=[]
                                    loc_now[0] = math.fmod(position[0],mapsize)
                                    loc_now[1]=position[0]-loc_now[0]
                                    
                                    u.update(loc_now[0],loc_now[1])
                                    i= u.check_angle()
                                    if(i==1):
                                        speech_funcs.PlaySpeech("TamNe")
                                    elif(i==2):
                                        speech_funcs.PlaySpeech("OtocSeDoprava")
                                    elif(i==3):
                                        speech_funcs.PlaySpeech("OtocSeDoleva")
                                    else:
                                        speech_funcs.PlaySpeech("JdiRovne")

                                    loc_now = User.user.TestPrezentace[key][0]
                                    loc_pred = User.user.TestPrezentace[key][1]
                                    u.update()
                                    u.check
                                    """
                                    d_y1 = loc_pred[1] - loc_now[1] # - to left, + to right
                                    d_x1 = loc_pred[0] - loc_now[0]

                                    d_y2 = loc_now[1] - loc_last[1]
                                    d_x2 = loc_now[0] - loc_last[0]

                                    #on X axis
                                    
                                    if (d_x1 < 0 or d_x1 > 0) and (d_x2 < 0 or d_x1 > 0):
                                        #transport relatively forward
                                        speech_funcs.PlaySpeech("JdiRovne")

                                    if d_x1 < 0 and d_y1 < 0:
                                        #transport forward and to left
                                        speech_funcs.PlaySpeech("OtocSeDoleva")

                                    if d_x1 < 0 and d_y1 > 0:
                                        #transport forward and to right
                                        speech_funcs.PlaySpeech("OtocSeDoprava")

                                    #on Y axis
                                    if (d_y1 < 0 or d_y1 > 0) and (d_y2 < 0 or d_y1 > 0):
                                        #transport relatively forward (i guess, TODO)
                                        speech_funcs.PlaySpeech("JdiRovne")

                                    if d_y1 < 0 and d_x1 < 0:
                                        #transport forward and to left
                                        speech_funcs.PlaySpeech("OtocSeDoleva")

                                    if d_y1 < 0 and d_x1 > 0:
                                        #transport forward and to right
                                        speech_funcs.PlaySpeech("OtocSeDoprava")
                                    """
                                    time.sleep(0.5)
                                    loc_last = User.user.TestPrezentace[key][0]

                                
                                position = f.find()

                                #track and repeat
                                break