import importlib
import sys
import types
import unittest
from pathlib import Path


PACKAGE_ROOT = (
    Path(__file__).resolve().parents[1] / "SerialDriver" / "SerialDriver"
)
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


class FakeSerialException(Exception):
    pass


class FakeSerialPort:
    def __init__(self):
        self.port = None
        self.baudrate = None
        self.bytesize = None
        self.parity = None
        self.stopbits = None
        self.timeout = None
        self.xonxoff = None
        self.rtscts = None
        self.dsrdtr = None
        self.writeTimeout = None
        self.open_called = False
        self.close_called = False
        self.next_read = b""
        self.next_line = b""
        self.raise_on = set()
        self.last_write = None
        self.isOpen = False

    def open(self):
        if "open" in self.raise_on:
            raise FakeSerialException("boom")
        self.open_called = True
        self.isOpen = True

    def write(self, data):
        if "write" in self.raise_on:
            raise FakeSerialException("boom")
        self.last_write = data

    def close(self):
        if "close" in self.raise_on:
            raise FakeSerialException("boom")
        self.close_called = True
        self.isOpen = False

    def read(self, size):
        if "read" in self.raise_on:
            raise FakeSerialException("boom")
        return self.next_read[:size]

    def readline(self):
        if "readline" in self.raise_on:
            raise FakeSerialException("boom")
        return self.next_line


def load_module():
    fake_serial_module = types.SimpleNamespace(
        Serial=FakeSerialPort,
        EIGHTBITS=8,
        PARITY_NONE="N",
        STOPBITS_ONE=1,
        serialutil=types.SimpleNamespace(SerialException=FakeSerialException),
    )
    sys.modules["serial"] = fake_serial_module

    sys.modules.pop("SerialDriver.SerialDriver", None)
    sys.modules.pop("SerialDriver.SerialDriverException", None)

    serial_driver_exception_module = importlib.import_module(
        "SerialDriver.SerialDriverException"
    )
    serial_driver_module = importlib.import_module("SerialDriver.SerialDriver")
    return (
        serial_driver_module.SerialDriver,
        serial_driver_exception_module.SerialDriverException,
    )


class SerialDriverTests(unittest.TestCase):
    def setUp(self):
        self.SerialDriver, self.SerialDriverException = load_module()
        self.driver = self.SerialDriver()

    def test_config_sets_expected_defaults(self):
        self.driver.config("/dev/ttyUSB0")

        self.assertEqual(self.driver.ser.port, "/dev/ttyUSB0")
        self.assertEqual(self.driver.ser.baudrate, 9600)
        self.assertEqual(self.driver.ser.bytesize, 8)
        self.assertEqual(self.driver.ser.parity, "N")
        self.assertEqual(self.driver.ser.stopbits, 1)
        self.assertEqual(self.driver.ser.timeout, 1)
        self.assertFalse(self.driver.ser.xonxoff)
        self.assertFalse(self.driver.ser.rtscts)
        self.assertFalse(self.driver.ser.dsrdtr)
        self.assertEqual(self.driver.ser.writeTimeout, 2)

    def test_open_close_and_status_delegate_to_serial_port(self):
        self.driver.open()
        self.assertTrue(self.driver.isOpen())

        self.driver.close()
        self.assertFalse(self.driver.isOpen())
        self.assertTrue(self.driver.ser.open_called)
        self.assertTrue(self.driver.ser.close_called)

    def test_is_open_supports_callable_serial_api(self):
        self.driver.ser.isOpen = lambda: True
        self.assertTrue(self.driver.isOpen())

    def test_write_encodes_data_as_utf16be(self):
        self.driver.write("Hola")
        self.assertEqual(self.driver.ser.last_write, "Hola".encode("utf-16be"))

    def test_read_returns_requested_bytes(self):
        self.driver.ser.next_read = b"abcdef"
        self.assertEqual(self.driver.read(3), b"abc")

    def test_read_line_returns_next_line(self):
        self.driver.ser.next_line = b"valor\n"
        self.assertEqual(self.driver.readLine(), b"valor\n")

    def test_open_wraps_serial_exceptions(self):
        self.driver.ser.raise_on.add("open")

        with self.assertRaisesRegex(
            self.SerialDriverException, "Error al abrir el puerto serie"
        ):
            self.driver.open()

    def test_write_wraps_serial_exceptions(self):
        self.driver.ser.raise_on.add("write")

        with self.assertRaisesRegex(
            self.SerialDriverException, "Error al escribir en el puerto serie"
        ):
            self.driver.write("Hola")

    def test_close_wraps_serial_exceptions(self):
        self.driver.ser.raise_on.add("close")

        with self.assertRaisesRegex(
            self.SerialDriverException, "Error al cerrar el puerto serie"
        ):
            self.driver.close()

    def test_read_wraps_serial_exceptions(self):
        self.driver.ser.raise_on.add("read")

        with self.assertRaisesRegex(
            self.SerialDriverException, "Error al leer del puerto serie"
        ):
            self.driver.read(1)

    def test_read_line_wraps_serial_exceptions(self):
        self.driver.ser.raise_on.add("readline")

        with self.assertRaisesRegex(
            self.SerialDriverException, "Error al leer del puerto serie"
        ):
            self.driver.readLine()


if __name__ == "__main__":
    unittest.main()
