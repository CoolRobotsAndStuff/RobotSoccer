from MainController import MainController
import time

controller = MainController(32)

while controller.doLoop():
    controller.run()
