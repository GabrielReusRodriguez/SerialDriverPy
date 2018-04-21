from SerialDriver.SerialDriver import SerialDriver
from SerialDriver.SerialDriverException import SerialDriverException 

import time

print ("init")

serialDrv = SerialDriver()
try:
    serialDrv.config("//./COM3")
    serialDrv.open()
    #time.sleep(1)
    #serialDrv.write("H")
    #time.sleep(3)
    #serialDrv.write("L")
    while ( True ):
        time.sleep(3)
        #datos = serialDrv.read(64)
        datos = serialDrv.readLine()
        if datos:
            print("Valor: ")
            print (datos)
            print ("\n")
    serialDrv.close()
except SerialDriverException as e:
    print(e)

print ("close")