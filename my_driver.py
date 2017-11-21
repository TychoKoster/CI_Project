from pytocl.driver import Driver
from pytocl.car import State, Command
import math

class MyDriver(Driver):
 # Override the `drive` method to create your own driver
	def drive(self, carstate: State) -> Command:
        	# Import data
		#data = carstate.tracks
		speed_x = carstate.speed_x
		speed_y = carstate.speed_y
		speed_z = carstate.speed_z
		speed = math.sqrt(speed_x**2 + speed_y**2 + speed_z**2)
		print(speed)
	       	#command = Command(...)
		return command
