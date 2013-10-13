import os
import glob
import time
import subprocess

class TempReader():
    def __init__(self): 
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
 
    def read_temp_raw(self, device_path):
        catdata = subprocess.Popen(['cat',device_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = catdata.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines
        
 
    def read_temp(self, device_path):
        if os.path.exists(device_path):
            lines = self.read_temp_raw(device_path)
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = self.read_temp_raw(device_path)
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                return temp_c, temp_f
        return 0.0, 0.0
            
if __name__ == "__main__":
    import sys
    tempReader = TempReader()
    print tempReader.read_temp(sys.argv[1])


    



        
