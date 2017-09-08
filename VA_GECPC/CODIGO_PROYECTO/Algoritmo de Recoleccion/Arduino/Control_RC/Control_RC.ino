// Se definen los pines que van a controlar la direccion.
const int adelante = 5;
const int atras = 6;
const int izq = 9;
const int der = 10;
char dir;

void setup() {
  /* Los pines reservados se definen como salidas y se inicia
  la comunicación serial a 115200 baudios. */
  pinMode(adelante, OUTPUT);
  pinMode(atras, OUTPUT);
  pinMode(izq, OUTPUT);
  pinMode(der, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  /* Si hay comunicación serial, se lee la información, se
  almacena el la variable dir y se compara para elegir la
  dirección con el método control(dir, tiempo).*/
  if (Serial.available()){
    dir = Serial.read();
    control(dir, 50);
  }
  /*De lo contrario, el vehiculo permanece apagado hasta 
  que se recibe otra señal.*/
  else
    apagar();
}

void avanzar(int duracion){
  digitalWrite(adelante, HIGH);
  delay(duracion);
}

void reversa(int duracion){
  digitalWrite(atras, HIGH);
  delay(duracion);
}

void derecha(int duracion){
  digitalWrite(der, HIGH);
  delay(duracion);
}

void izquierda(int duracion){
  digitalWrite(izq, HIGH);
  delay(duracion);
}

void giro_derecha(int dd, int da){
  digitalWrite(der, HIGH);
  digitalWrite(adelante, HIGH);
  delay(da);
  digitalWrite(adelante, LOW);
  delay(dd - da);
}

void giro_izquierda(int di, int da){
  digitalWrite(izq, HIGH);
  digitalWrite(adelante, HIGH);
  delay(da);
  digitalWrite(adelante, LOW);
  delay(di - da);
}

void giro_derecha(int duracion){
  digitalWrite(der, HIGH);
  digitalWrite(adelante, HIGH);
  delay(duracion);
}

void giro_izquierda(int duracion){
  digitalWrite(izq, HIGH);
  digitalWrite(adelante, HIGH);
  delay(duracion);
}

void atras_derecha(int duracion){
  digitalWrite(atras, HIGH);
  digitalWrite(der, HIGH);
  delay(duracion);
}

void atras_izquierda(int duracion){
  digitalWrite(atras, HIGH);
  digitalWrite(izq, HIGH);
  delay(duracion);
}

void apagar(){
  digitalWrite(adelante, LOW);
  digitalWrite(atras, LOW);
  digitalWrite(izq, LOW);
  digitalWrite(der, LOW);
}

void control(char direccion, int duracion){
  switch (direccion){
     case '0':
      apagar(); 
     break;
     
     case '1': 
      avanzar(duracion); 
     break;
     
     case '2': 
      reversa(duracion);
     break;
     
     case '3': 
      derecha(duracion);
     break;
     
     case '4': 
      izquierda(duracion); 
     break;
     
     case '6': 
      giro_derecha(70, duracion);
     break;
     
     case '7': 
      giro_izquierda(70, duracion);
     break;

     case '8': 
      atras_derecha(duracion); 
     break;

     case '9': 
      atras_izquierda(duracion); 
     break;
    }
}
