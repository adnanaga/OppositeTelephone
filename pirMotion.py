import time
from gpiozero import MotionSensor
from gpiozero import Button
from gpiozero import Motor
from signal import pause
import os
from twilio.rest import Client
import sys

# Setup variables
account_sid = "AC055d249bea408ca762879952ffdb2bc1"
auth_token = "3285301a87f28ed952e5822cb0a74fc6"
client = Client(account_sid, auth_token)


clicker = Button(20)
c1 = Button(0)
c2 = Button(5)
c3 = Button(6)
#c4 = Button(4)
r1 = Button(16)
r2 = Button(19)
r3 = Button(26)
r4 = Button(21)

pickupSwitch = Button(14)
motor = Motor(23, 24)

pir = MotionSensor(4)
pickedUp = False
ringing = False

phoneNumber = ''

def convertToCode(code):
    
    global phoneNumber
    num = ''

    if (code == "1000000"):
#         num = ('rest')
        print('')
    
    elif (code == "0100010"):
        num = ('1')
    
    elif (code == "0010010"):
        num = ('2')
    
    elif (code == "0100001"):
        num = ('3')
    
    elif (code == "0010001"):
        num = ('4')
    
    elif (code == "1000001"):
        num = ('5')
    
    elif (code == "0000001"):
        num = ('6')
    
    elif (code == "0000000"):
        num = ('7')
    
    elif (code == "1001000"):
        num = ('8')
    
    elif (code == "0101000"):
        num = ('9')
        
    elif (code == "0011000"):
        num = ('0')
        
    elif (code == "1000100"):
        num = ('#')
        
    elif (code == "0100100"):
        num = ('*')
            
    if len(phoneNumber) <= 9:
        phoneNumber = phoneNumber + num
        print(phoneNumber)
        statement = 'echo "{}" | festival --tts'.format(num)
        os.system(statement)
        
    if len(phoneNumber) == 10:
        print('your phone number is' + phoneNumber)
        statement = 'echo "Your phone number is {}" | festival --tts'.format(phoneNumber)
        os.system(statement)
        lookup(phoneNumber)
         

def waitForNumber():
    print("waiting for number")
    clicker.when_pressed = checkPins
    
def checkPins():
    print("checking pins")
    C1Val = c1.is_pressed
    C1Val = not C1Val
    R1Val = r1.is_pressed
    R1Val = not R1Val
    
    C2Val = c2.is_pressed
    C2Val = not C2Val
    R2Val = r2.is_pressed
    R2Val = not R2Val
    
    C3Val = c3.is_pressed
    C3Val = not C3Val
    R3Val = r3.is_pressed
    R3Val = not R3Val
    
#    C4Val = c4.is_pressed
#    C4Val = not C4Val
    R4Val = r4.is_pressed
    R4Val = not R4Val
    
    finalCode = "" + str(int(C1Val))+ str(int(C2Val)) + str(int(C3Val)) + str(int(R1Val)) + str(int(R2Val)) + str(int(R3Val)) + str(int(R4Val))
    convertToCode(finalCode)
    

def ring():
    global ringing
    global pickedUp
    
    print("Ringing" + str(ringing))
    print("pickedUp" + str(pickedUp))
    
    if not (ringing):
        print('ringing')
        ringing = True
        # when they pick up phone we go to pickup function
        pickup()
    else:
        print('Phone still in use')
        
def pickup():
    global pickedUp
    print(pickupSwitch.is_pressed)
    while not pickedUp:
        print('phone still ringing')
#         motor.forward()
#         time.sleep(0.2)
#         motor.stop()
#         motor.forward()
#         time.sleep(0.2)
#         motor.stop()
#         time.sleep(1)
        pickedUp = pickupSwitch.is_pressed

#     motor.stop()
    print('Phone picked up')
    os.system('echo "Hello, I am the Operator of everything. I know who you are. If you do not believe me, dial your phone number!" | festival --tts')

    waitForNumber()
    
def lookup(num):
    global ringing
    global pickedUp
    global phoneNumber
    try:
        phone_number = client.lookups \
                   .v1 \
                   .phone_numbers("+1" + num) \
                   .fetch(add_ons=['ekata_reverse_phone'])
        name = phone_number.add_ons["results"]["ekata_reverse_phone"]["result"]["belongs_to"]["name"]
        statement = 'echo "Thank you for answering {}" | festival --tts'.format(name)
    except:
        statement = 'echo "Thank you for answering, I cannot find your name. You win" | festival --tts'        
    
    print(statement)
    os.system(statement)
    time.sleep(1)
    os.system('echo "Goodbye" | festival --tts')
#     os.system('speaker-test -c2 -t sine -f 200')
    time.sleep(5)
    print('setting ringing to false and reseting phone number')
    pickedUp = False
    ringing = False
    phoneNumber = ''

def restart():
    os.execl(sys.executable, sys.executable, *sys.argv)

def main():
    global ringing
    global pickedUp
    
    print("Starting phone program!")

    pir.when_motion = ring
    pickupSwitch.when_released = restart
    pause()

main()