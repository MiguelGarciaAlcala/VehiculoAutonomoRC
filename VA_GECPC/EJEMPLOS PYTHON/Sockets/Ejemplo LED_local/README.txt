COMUNICACIÓN SERIAL PYTHON-ARDUINO
Para ejecutar el ejemplo es necesario:
1. Conectar Arduino y montar un circuito con dos LED's conectados a
    los pines que les corresponden.
2. Ejecutar el programa LED.ino ubicado en la carpeta Arduino/LED
3. Editar el archivo LED_Servidor.py ubicado en la carpeta Python:
    a) Colocar la IP del servidor local en la variable HOST.
    b) Ingresar el puerto serial al que se conectó Arduino. 
    Por defecto es:
         arduino = serial.Serial('COM5', 115200)
    pero el parámetro 'COM1, COM2, ...., COMN' puede variar en función 
    del sistema operativo que estemos usando.
4. Habilitar el servidor LED_Servidor.py.
5. Modificar el archivo LED_Cliente.py ubicado en la carpeta Python:
    a) Colocar la dirección IP del servidor local en la variable HOST.
    b) Verificar que la variable PUERTO tenga el mismo valor que su homónimo
    en el archivo LED_Servidor.py.
6. Copiar el archivo LED_Cliente.py en Raspberry Pi y ejecutarlo.
7. Ingresar algunos caracteres para verificar que la conexión es correcta.