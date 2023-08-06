import time
pi = 3.1415926536
e = 2.7182818284
def areaofcircle_d(d):
    print(d*3.1415926536)
def areaofcircle_r(r):
    print(2*r*3.1415926536)
version='0.0.1'
def delay(t):
    time.sleep(t)
def makeadatalog(name):
    name=open(name,"w+")
def help():
    print('commands')
    print('defined PI')
    print('defined E')
    print('perimeterofcircle_d --- calculate the perimeter of a circle using the diameter ---syntax = perimeterofcircle_d(diameter)')
    print('perimeterofcircle_d --- calculate the perimeter of a circle using the radius --- syntax = perimeterofcircle_r(radius)')
    print('defined delay function --- syntax = delay(seconds) ')