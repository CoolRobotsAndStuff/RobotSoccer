from mainController import mainController
import time

controller = mainController(32)

while controller.doLoop():
    controller.run()
