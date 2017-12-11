#! /usr/bin/env python3

from pytocl.main import main
#from pytocl.driver import DriverP
from Swarm_MyDriver import MyDriverMLP


if __name__ == '__main__':
	main(MyDriverMLP())

