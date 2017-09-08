// Control por teclado.

const int adelante = 5;
const int atras = 6;
const int izq = 9;
const int der = 10;
char dir = '0';

void setup() {
  pinMode(adelante, OUTPUT);
  pinMode(atras, OUTPUT);
  pinMode(izq, OUTPUT);
  pinMode(der, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available())
    control(Serial.read(), 40);
  else apagar();
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

void giro_derecha(int duracion){
  digitalWrite(adelante, HIGH);
  digitalWrite(der, HIGH);
  delay(duracion);
}

void giro_izquierda(int duracion){
  digitalWrite(adelante, HIGH);
  digitalWrite(izq, HIGH);
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
      giro_derecha(duracion);
     break;
     
     case '7': 
      giro_izquierda(duracion); 
     break;
     
     case '8': 
      atras_derecha(duracion); 
     break;
     
     case '9': 
      atras_izquierda(duracion); 
     break;
    }
}
