from SpeechRec import speech_funcs
from localization import finder, serial_scanner

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

source = speech_funcs.sr.Microphone()
speech_funcs.Recognizer.adjust_for_ambient_noise(source)
while True:
    # if "začal se pohybovat:"
    #
    #
    #speech_funcs.PlaySpeech("KamJdes")

    Commands = speech_funcs.SpeechToText(source)
    if len(Commands) == 0: #skipoing empty command
        continue

    Command_buffer.extend(Commands)
    print(Command_buffer)
    #nějaké vyhodnocení a nalezení místnosti
    for y_data in Desired_Data:
        for data in y_data:
            if data in Command_buffer: #We found desired word!
                word = data

                #locate word (pokoj)
                #
                #
                #
                Finder = finder()
                position, reg_len = Finder.find()
