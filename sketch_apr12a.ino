const int NUM_BUTTONS = 3;
const int LED_PINS[] = {3, 4, 5};
const int BUTTON_PINS[] = {11, 12, 13};
const int POT_PIN = A0;
bool buttonStates[NUM_BUTTONS] = {true};

void setup() {
  // Configurar pines de LEDs como salida
  for (int i = 0; i < sizeof(LED_PINS) / sizeof(LED_PINS[0]); i++) {
    pinMode(LED_PINS[i], OUTPUT);
    digitalWrite(LED_PINS[i], LOW); // Apagar todos los LEDs al inicio
  }

  // Configurar pines de botones como entrada
  for (int i = 0; i < sizeof(BUTTON_PINS) / sizeof(BUTTON_PINS[0]); i++) {
    pinMode(BUTTON_PINS[i], INPUT_PULLUP);
  }
  Serial.begin(9600);
}

void loop() {
  // Leer valor analógico del potenciómetro
  int potValue = analogRead(POT_PIN);
  Serial.print(potValue);
  Serial.print(",");

  // Leer estado de los botones y actualizar array de estados
  for (int i = 0; i < NUM_BUTTONS; i++) {
    // Leer estado del botón y aplicar debounce
    bool buttonState = digitalRead(BUTTON_PINS[i]);
    delay(50); // Esperar un corto tiempo para el debounce
    buttonState = digitalRead(BUTTON_PINS[i]);
    
    // Enviar estado del botón por el puerto serie
    Serial.print(buttonState ? "1" : "0"); 
    Serial.print(",");
    
    // Actualizar array de estados de botones
    buttonStates[i] = buttonState;
  }
  Serial.println();

  delay(100); // Esperar un breve periodo antes de la siguiente iteración del loop
}

