// Comunicación serial a través de Raspberry Pi.

// Se reservan los pines 12 y 13 de Arduino.
const int LED1 = 12;
const int LED2 = 13;

void setup() {
  // Se habilita la comunicación serial con una velocidad de 155200 bits 
  // por segundo (baudios) y se configuran los pines 12 y 13 como salida.
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  if(Serial.available()){
    // Si el puerto serial está disponible, inicia la lectura de datos.
    switch(Serial.read()){
      // Cuando el servidor envia un 1, se enciende el LED1. Si recibimos un 2, se enciende el LED2.
      // Los caracteres a y b apagan los LED's 1 y 2, respectivamente.
      case '1':
        digitalWrite(LED1, HIGH);
        break;
      case '2':
        digitalWrite(LED2, HIGH);
        break;
      case 'a':
        digitalWrite(LED1, LOW);
        break;
      case 'b':
        digitalWrite(LED2, LOW);
        break;
    }
  }
}
