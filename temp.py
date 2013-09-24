import os
import os.path
import glob
import time
import subprocess
import RPi.GPIO as GPIO
from time import gmtime, strftime
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
fridge_path = "/sys/bus/w1/devices/28-0000046186c3/w1_slave"
fridge_channel = 11
s1_path = "/sys/bus/w1/devices/28-00000501d367/w1_slave"
s1_channel = 12
s2_path = "/sys/bus/w1/devices/28-00000500e5b9/w1_slave"
s2_channel = 15


def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)

def read_temp_raw(device_path):
	catdata = subprocess.Popen(['cat',device_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err = catdata.communicate()
	out_decode = out.decode('utf-8')
	lines = out_decode.split('\n')
	return lines
 
def read_temp(device_path):
    lines = read_temp_raw(device_path)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_path)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def control(path, pin, set_temp):
    temp_c, temp_f = read_temp(path)
    if (set_temp - 1 < temp_f):
        GPIO.output(pin, True)
    elif (set_temp >= temp_f):
        GPIO.output(pin, False)
    return temp_f
	
if __name__ == "__main__":
    init_gpio()

    log_path = '/home/pi/temp.log'
    
    if not os.path.isfile(log_path):
        f = open(log_path, 'w')
        f.close()
    
    while True:
        fridge_temp = control(fridge_path, fridge_channel, 40.0)
        s1_temp = control(s1_path, s1_channel, 62.0)
        s2_temp = control(s2_path, s2_channel, 66.0)
        temps = '\t'.join([strftime("%Y-%m-%d %H:%M:%S", gmtime()), str(fridge_temp), str(40.0), str(s1_temp), str(62.0), str(s2_temp), str(66.0)])
        print temps
        f = open(log_path, 'a')
        f.write(temps)
        f.write('\n')
        f.close()
        time.sleep(5)


        
