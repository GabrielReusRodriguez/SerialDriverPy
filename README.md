# SerialDriverPy

Librería sencilla en Python para comunicarse con Arduino y otros dispositivos por puerto serie usando `pyserial`.

## Estructura del proyecto

```text
SerialDriverPy/
├── README.md
├── SerialDriver/
│   └── SerialDriver/
│       ├── main.py
│       └── SerialDriver/
│           ├── SerialDriver.py
│           ├── SerialDriverException.py
│           └── __init__.py
└── tests/
    └── test_serial_driver.py
```

## Requisitos

- Python 3
- `pyserial` para usar el driver con un puerto serie real

## Instalación

```bash
pip install pyserial
```

Si vas a importar el paquete desde la raíz del repositorio, añade la carpeta del proyecto a `PYTHONPATH`:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/SerialDriver/SerialDriver"
```

## Uso básico

```python
from SerialDriver.SerialDriver import SerialDriver
from SerialDriver.SerialDriverException import SerialDriverException

driver = SerialDriver()

try:
    driver.config("/dev/ttyUSB0")
    driver.open()
    driver.write("H")
    respuesta = driver.readLine()
    print(respuesta)
    driver.close()
except SerialDriverException as error:
    print(error)
```

En Windows puedes usar un puerto con formato `//./COM3`, tal y como aparece en el ejemplo incluido en `main.py`.

## API disponible

### `SerialDriver`

- `config(portName)`: configura el puerto y los valores por defecto de comunicación:
  - baudrate: `9600`
  - bytesize: `8`
  - parity: `none`
  - stopbits: `1`
  - timeout de lectura: `1s`
  - timeout de escritura: `2s`
- `open()`: abre el puerto serie
- `write(data)`: envía una cadena codificada en UTF-16 big endian
- `read(size)`: lee la cantidad de bytes indicada
- `readLine()`: lee una línea completa
- `close()`: cierra el puerto
- `isOpen()`: indica si el puerto está abierto

### `SerialDriverException`

Excepción usada para encapsular errores de apertura, escritura, lectura y cierre del puerto serie.

## Ejemplo incluido

El archivo `/home/runner/work/SerialDriverPy/SerialDriverPy/SerialDriver/SerialDriver/main.py` muestra un ejemplo de lectura continua desde `//./COM3`.

## Pruebas

Las pruebas automáticas usan `unittest` y simulan el puerto serie, por lo que no necesitan hardware real ni `pyserial` instalado.

Para ejecutarlas desde la raíz del repositorio:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Observaciones de la revisión

- El proyecto implementa un wrapper muy ligero sobre `pyserial`.
- La lógica de negocio está concentrada en `SerialDriver.py`.
- El ejemplo actual en `main.py` está pensado para pruebas manuales con hardware conectado.
