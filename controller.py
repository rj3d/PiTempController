import time
import RPi.GPIO as GPIO
from config_reader import Config
from temp_reader import TempReader

class Controller:
    def init_gpio(self):
        o_states = {}
        GPIO.setmode(GPIO.BOARD)
        for ioConfig in self.config.io:
            GPIO.setup(ioConfig.o_pin, GPIO.OUT)
            o_states[ioConfig.o_pin] = 0
        return o_states

    def __init__(self, config_path):
        self.config = Config(config_path)
        self.tempReader = TempReader()
        self.o_states = self.init_gpio()
        
    def cur_dt_str(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
    def control(self, ioConfig):
        temp_c, temp_f = self.tempReader.read_temp(ioConfig.i_path)
        if (ioConfig.set_temp < temp_f):
            GPIO.output(ioConfig.o_pin, True)
            self.o_states[ioConfig.o_pin] = 1
        elif (ioConfig.set_temp - ioConfig.buffer_temp >= temp_f):
            GPIO.output(ioConfig.o_pin, False)
            self.o_states[ioConfig.o_pin] = 0
        return temp_f
    
    def run(self):
        while True:
            log_lst = [self.cur_dt_str()]

            for ioConfig in self.config.io:
                cur_temp = self.control(ioConfig)
                log_lst.append(str(cur_temp))
                log_lst.append(str(ioConfig.set_temp))
                log_lst.append(str(self.o_states[ioConfig.o_pin]))
                
            log_line = '\t'.join(log_lst)
            print log_line
            f = open(self.config.log_path, 'a')
            f.write(log_line)
            f.write('\n')
            f.close()
            
            time.sleep(5)

if __name__ == "__main__":
    import sys
    c = Controller(sys.argv[1])
    c.run()