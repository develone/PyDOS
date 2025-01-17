import sys
from pydos_ui import Pydos_ui
try:
    from pydos_ui import input
except:
    pass
if sys.implementation.name.upper() == 'MICROPYTHON':
    import machine
    from time import ticks_ms
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    from supervisor import ticks_ms
    from pwmio import PWMOut
    foundPin = True
    try:
        #A5 is GPIO D19 on Nano Connect
        from board import A5 as sndPin
    except:
        foundPin = False
    if not foundPin:
        foundPin = True
        try:
            #Use D12 on Feather
            from board import D12 as sndPin
        except:
            foundPin = False

def piano():

    if sys.implementation.name.upper() == 'MICROPYTHON':
        pwm=machine.PWM(machine.Pin(19))
    elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
        pwm=PWMOut(sndPin, duty_cycle=0, frequency=440, variable_frequency=True)

    print ("\nPress +/- to change volume, 'q' to quit...")

    volume = 400
    cmnd = None
    press = False
    noneAt = ticks_ms()
    firstNone = True
    note = 0
    while cmnd != "q":
        if Pydos_ui.serial_bytes_available() != 0:
            cmnd = Pydos_ui.read_keyboard(1)
            #print("->"+cmnd+"<- : ",ord(cmnd[0]))
            firstNone = True
            if cmnd=="h": # middle C
                note=int(261.6256+.5)
                press = True
            elif cmnd == "a": # E
                note=int(164.8138+.5)
                press = True
            elif cmnd == "s": # F
                note=int(174.6141+.5)
                press = True
            elif cmnd == "d": # G
                note=int(195.9977+.5)
                press = True
            elif cmnd == "r": # G sharp/A flat
                note=int(207.6523+.5)
                press = True
            elif cmnd == "f": # A
                note=int(220)
                press = True
            elif cmnd == "t": # A sharp/B flat
                note=int(233.0819+.5)
                press = True
            elif cmnd == "g": # B
                note=int(246.9417+.5)
                press = True
            elif cmnd == "u": # C sharp/D flat
                note=int(277.1826+.5)
                press = True
            elif cmnd == "j": # D
                note=int(293.6648+.5)
                press = True
            elif cmnd == "k": # E
                note=int(329.6276+.5)
                press = True
            elif cmnd == "l": # F
                note=int(349.2262+.5)
                press = True
            elif cmnd == "o": # F sharp/G flat
                note=int(369.9944+.5)
                press = True
            elif cmnd == ";": # G
                note=int(391.9954+.5)
                press = True
            elif cmnd == "q":
                break

            if cmnd == "+":
                volume += 100
            elif cmnd == "-":
                volume -= 100
        else:
            if firstNone:
                noneAt = ticks_ms()
                firstNone = False
            else:
                if ticks_ms() > noneAt+500:
                    firstNone = True
                    press = False

        if press:
            if sys.implementation.name.upper() == 'MICROPYTHON':
                pwm.freq(note)
                pwm.duty_u16(volume)
            elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
                pwm.frequency = note
                pwm.duty_cycle = volume

            #time.sleep(.1)
            #cmnd = kbdInterrupt()
            #while cmnd != None:
                #cmnd = kbdInterrupt()
            #pressedat = time.time()
        else:
            if sys.implementation.name.upper() == 'MICROPYTHON':
                pwm.duty_u16(0)
            elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
                pwm.duty_cycle = 0
            #print("Release")

    if sys.implementation.name.upper() == 'CIRCUITPYTHON':
        pwm.deinit()

piano()
