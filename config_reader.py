class IoConfig:
	def __init__(self, i_path, mode, o_pin=None, set_temp=None, buffer_temp=None, direction=None):
		self.i_path = i_path
		self.mode = mode
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
			return lambda t: self.set_temp + self.buffer_temp <= t
		return None

	def __repr__(self):
		return 'IoConfig()'

	def __str__(self):
		str_lst = ['Input path:', str(self.i_path),
			'Mode:', str(self.mode),
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
			if len(splat) == 1:
				self.io.append( IoConfig( temp_path % { "TEMP" :splat[0] },
					'MONITOR'
				) )
			else:
				self.io.append( IoConfig( temp_path % { "TEMP" :splat[0] },
					'CONTROLLER',
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
