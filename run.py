#! /usr/bin/env python3

from pytocl.main import main
from pytocl.driver import Driver
from my_driver import MyDriver
from my_driver_mlp import MyDriverMLP

if __name__ == '__main__':
    # main(MyDriver())
    main(MyDriverMLP())
    # main(Driver(logdata=True))
