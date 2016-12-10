from SimpleCV import Color,Camera,Display
import RPi.GPIO as GPIO
import time
from smbus import SMBus


bus = SMBus(1)
bus2 = SMBus(1)
bus3 = SMBus(1)


cam = Camera() #starts the camera
display = Display()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

def Green():
    GPIO.output(11,True)
    GPIO.output(12,False)
    time.sleep(2)
    

def Red():
    GPIO.output(11,False)
    GPIO.output(12,True)
    
def vol():
    print("Read the A/D")
    bus.write_byte(0x48, 3) # set control register to read channel 3(potienmeter or "volt meter")
    last_reading = -1
    reading = bus.read_byte(0x48) # read A/D
    if(abs(last_reading - reading) > 2):
        last_reading = reading
        voltage = ((last_reading *5)/256.0)
        print("Analog voltage : %s" % last_reading)
        print 'Voltage : {percent:.2}V'.format(percent = (last_reading *5)/256.0)
  	
def light():
    print("Read the Light")
    bus2.write_byte(0x48, 0) # set control register to read channel 0(light sensor)
    last_reading = -1
    reading = bus2.read_byte(0x48) 
    if(abs(last_reading - reading) > 2):
        print("Analog Light : %s" % reading)

def temp():
    print("Read the temperature")
    bus3.write_byte(0x48, 1)  # set control register to read channel 1(temp sensor)
    last_reading = -1 
    reading = bus3.read_byte(0x48)
    if(abs(last_reading - reading) > 2):
        print("Analog Temperature : %s" % reading)




while(display.isNotDone()):
    Red()
    img = cam.getImage() # get image from the camera

    barcode = img.findBarcode() #finds barcode data from image
    if(barcode is not None):
        barcode = barcode[0]
        result = str(barcode.data)
        Green()
        if(result == "Voltage"):
            vol()
        if(result == "Temp"):
            temp()
        if(result == "Light"):
            light()
        print result # print result of barcode in python shell
        barcode = [] # reset the barcode

    img.save(display) #shows the image on the screen
    
