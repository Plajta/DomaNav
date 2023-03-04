#custom imports:
from SpeechRec import speech_funcs
from localization import finder
from navigace import Node, controlAccel, graf, user #TODO: i have to repair that COM3 problem
import time

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

Desired_Data = [["postel", "posteli", "postelí", "postele"], #ano, všechno jsem to vyskloňoval...
                ["stůl", "stolu", "stolem"],
                ["křeslo", "křesla", "křeslu", "křeslem"],
                ["televize", "televizi", "televizí"],
                ["záchod", "záchodu", "záchodě", "záchodem"],
                ["lednice", "lednici", "lednicí"],
                ["kuchyň", "kuchyně", "kuchyní", "kuchyni"],
                ["koupelna", "koupelny", "koupelně", "koupelnu", "koupelnou"],
                ["ložnice", "ložnici", "ložnicí"]]


for i in range(0, speech_funcs.numdevices):
    if (speech_funcs.Pyaudio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", speech_funcs.Pyaudio.get_device_info_by_host_api_device_index(0, i).get('name'))


#
# MAIN
#

micro_object = controlAccel.setup()
with speech_funcs.sr.Microphone() as source:
    speech_funcs.Recognizer.adjust_for_ambient_noise(source)
    while True:

        data = controlAccel.GetData(micro_object)
        if data:
            if last_deg != 0:
                d_deg = abs(int(last_deg) - int(data.replace("\n", "")))
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
                for y_data in Desired_Data:
                    for data in y_data:
                        if data in Command_buffer: #We found desired word!
                            word = data

                            if word == "lednice": #pro teď budeme používat jenom 1 class
                                for key in user.TestPrezentace:
                                    print(key) #TODO: dodělat
                                Finder = finder()
                                position, reg_len = Finder.find()

                                #convert path to spoken word
                                #
                                #
                                #

                                #track and repeat
                                break