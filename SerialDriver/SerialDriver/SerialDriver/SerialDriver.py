
import serial
from SerialDriver.SerialDriverException import SerialDriverException

class SerialDriver:
    """Clase que implementa el Driver para comunicarse con un puerto serie""" 

    def __init__(self):
        self.ser = serial.Serial()

    def config(self,portName):
        #ser.port = "/dev/ttyUSB0"
        self.ser.port = portName
        #ser.port = "/dev/ttyS2"
        self.ser.baudrate = 9600
        self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        self.ser.parity = serial.PARITY_NONE #set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        #ser.timeout = None          #block read
        self.ser.timeout = 1            #non-block read
        #ser.timeout = 2              #timeout block read
        self.ser.xonxoff = False     #disable software flow control
        self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 2     #timeout for write

    def open(self):
        try:
            self.ser.open()
        except serial.serialutil.SerialException as e:
            raise SerialDriverException("Error al abrir el puerto serie")

    def write(self, data):
        try:
            self.ser.write(bytes(data,'utf-16be'))
        except serial.serialutil.SerialException as e:
            raise SerialDriverException("Error al escribir en el puerto serie")
    
    def close(self):
        try:
            self.ser.close()
        except serial.serialutil.SerialException as e:
            raise SerialDriverException("Error al cerrar el puerto serie")

    def isOpen(self):
        return self.ser.isOpen

    def read(self,size):
        try:
            return self.ser.read(size)
        except serial.serialutil.SerialException as e:
            raise SerialDriverException("Error al leer del puerto serie")
    def readLine(self):
        try:
            return self.ser.readline()
        except serial.serialutil.SerialException as e:
            raise SerialDriverException("Error al leer del puerto serie")