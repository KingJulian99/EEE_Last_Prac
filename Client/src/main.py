import busio
import time
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import RPi.GPIO as GPIO
import sys
import socket

global chan0, chan1, step, s, status

# Prints out the values read from the thermistor and LDR.
def check_and_print(name):
    global chan1, step, status
    status = 1

    print("Runtime\t\tTemp Reading\t\tTemp\t\tLight Reading")

    start = time.time()
    adc_light, adc_temp = get_new_vals()
    temp = get_temp(chan1.voltage)
    value = 0
    print_out(adc_temp, temp, adc_light, value)

    send(adc_temp, temp, adc_light, value)
    
    while(status == 1):

        diff = int(time.time() - start)

        # Checking to see whether enough time has passed.
        if (diff >= step):

            value += step
            adc_light, adc_temp = get_new_vals()
            temp = get_temp(chan1.voltage)
            print_out(adc_temp, temp, adc_light, value)
            send(adc_temp, temp, adc_light, value)
            start = time.time()
        
# Connects to the server through tcp.    
def connect():
    # Specifying the ip and port of the server.
    ip = "156.155.137.65"
    port = 5005
        
    s.connect((ip, port))
    message = s.recv(1024)
    
    while (message != 1):
        continue
    check_and_print()

    
# Closes the tcp connection to the server.
def close():
    s.close()

# Sends sensor info to the server through tcp.
def send(adc_temp, temp, adc_light, value):

    buffer = 1024
    data = adc_temp + "-" + temp + "-" + adc_light + "-" + value
    
    s.send(data)
    confirm = s.recv(buffer)
    
    # Checking whether the server received the message or not.
    while ("Y" not in confirm):
        
        # Closes connection to server if receives a 'X' indicating the server is going offline.
        if ("X" in confirm):
            close()
        elif (confirm == 0):
            status = 0
        elif ("S" in confirm):
            if (status == 1):
                s.send("ON")
            else:
                s.send("OFF")
        else:
            print("Data not received. \nResending data...")
            s.send(data)
            confirm = s.recv(buffer)
            
        
    print("Data received.")

# Function returns the raw ADC values of thermistor and LDR.
def get_new_vals():
    adc_light_value = chan0.value
    adc_temp_value = chan1.value

    return adc_light_value, adc_temp_value

# Calculates the temperature using the passed voltage.
def get_temp(voltage):
    
    # Equation used: Ta = (Tc - V0c) / Tc
    # Values found on the MCP9700 data sheet.
    temp = 0
    temp = round((voltage - 0.5) / 0.01, 2)

    return temp

# Formats the values to be printed out.
def print_out(temp_v, temp, light_v, timeCount):
    print(f"{timeCount}\t\t{temp_v}      \t\t{temp} C\t\t{light_v}")

if (__name__=="__main__"):

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel on pin 3 (light)
    chan0 = AnalogIn(mcp, MCP.P2)

    # create an analog input channel on pin 2 (temp)
    chan1 = AnalogIn(mcp, MCP.P1)

    step = 10
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status = 0

    try:
        th = threading.Thread(target=connect, args=(1, ), daemon=True)
        th.start()
        th.join()
    finally:
        close()
        GPIO.cleanup()