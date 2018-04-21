class SerialDriverException(Exception):
    """Excepciones encapsuladas en una sola excepcion"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

