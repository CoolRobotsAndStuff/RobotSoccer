from mainController import MainController

timeStep = 32
controller = MainController(timeStep)

while controller.doLoop():
    controller.run()
