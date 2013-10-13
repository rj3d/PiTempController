class IoConfig:
	def __init__(self, i_path, o_pin, set_temp, buffer_temp, direction):
		self.i_path = i_path
		self.o_pin = o_pin
		self.set_temp = set_temp
		self.buffer_temp = buffer_temp
		self.on_fn = self.get_on_fn(direction)
		self.off_fn = self.get_off_fn(direction)

	def get_on_fn(self, direction):
		if direction == '-':
			return lambda t: self.set_temp < t
		elif direction == '+':
			return lambda t: self.set_temp > t
		return None
		
	def get_off_fn(self, direction):
		if direction == '-':
			return lambda t: self.set_temp - self.buffer_temp >= t
		elif direction == '+':
			return lambda t: self.set_temp - self.buffer_temp <= t
		return None

	def __repr__(self):
		return 'IoConfig()'

	def __str__(self):
		str_lst = ['Input path:', str(self.i_path),
			'Output pin:', str(self.o_pin),
			'Set temp:', str(self.set_temp),
			'Buffer temp:', str(self.buffer_temp)
		]
		return '\t'.join(str_lst)

class Config:
	def __init__(self, config_path, temp_path = '/sys/bus/w1/devices/%(TEMP)s/w1_slave'):
		f = open(config_path)
		self.log_path = f.readline().strip()
		self.io = []
		for line in f:
			splat = line.strip().split()
			self.io.append( IoConfig( temp_path % { "TEMP" :splat[0] },
				int(splat[1]),
				float(splat[2]),
				float(splat[3]),
				splat[4]
			) ) 
		f.close()

	def __repr__(self):
		return 'Config()'

	def __str__(self):
		str_lst = [ 'Log path:',
			self.log_path,
			'IO Configs:',
			'\n'.join([str(c) for c in self.io])
		]
		return '\n'.join(str_lst)
		
if __name__ == "__main__":
	import sys
	config = Config(sys.argv[1])
	print config
			