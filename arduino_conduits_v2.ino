#include <QueueList.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>

// setting all variables
// constants won't change. They're used here to set pin numbers:
const int buttonPin = 2;    // the number of the pushbutton pin
const int unlockPin = 11;      // number of pin connected to *unlock* on remote
const int ledunlockPin = 14;      // number of pin connected to *unlock* on remote
const int lockPin = 12;      // number of pin connected to *lock* on remote
const int ledlockPin = 15;      // number of pin connected to *lock* on remote
const int ledPin = 13;      // the number of the LED pin

// the following variables are unsigned longs because the time, measured in
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 40;    // the debounce time; increase if the output flickers

// lists and other variables
//password goes backwards, read right to left
long passwordList[6] = {1000, 500, 500, 500, 500, 500};

// main temporary variables
int button = 0;
int last_button = 0;
bool lock_timer_start = false;
unsigned long lock_clock_time = millis();
unsigned long idle_clock_time = millis();
int button_state = 0;
long button_press_value = 0;
int unlockList[6] = {0, 0, 0, 0, 0, 0};
long passwordEnterList[6] = {100000, 100000, 100000, 100000, 100000, 100000};

//functions/procedures -----------------------------------------

//button detect function 
int GPIOBUTTONDETECT(){
  if (digitalRead(buttonPin) == HIGH){
    button = 1;
  }  
  
  else{
    button = 0;
  }

  if ((button == 1) && (last_button == 0)){
    last_button = button;
    return (1);
  }
   
  else if ((button == 0) && (last_button == 1)){
    last_button = button;
    return (2);
  }

  else {
    return (0);
  }
}

//push function
int pushEnterList(int newVal){
  for (int i = 5; i > 0; i--){
    passwordEnterList[i] = passwordEnterList[i-1];
  }
  passwordEnterList[0] = newVal;
  digitalWrite(ledPin, HIGH);
  delay(50);
  digitalWrite(ledPin, LOW);
}

//sleep function
void sleepNow(){
  Serial.println("\n\nsleep\n\n");
  delay(15);
  sleep_enable();
  attachInterrupt(digitalPinToInterrupt(2), wakeUpNow, HIGH); //set button 2 to wake up arduino
  set_sleep_mode (SLEEP_MODE_PWR_DOWN); //set sleep mode
  sleep_mode(); //actually sleeps
  //sleeping at this time, when inturruped by button, code below runs
  sleep_disable();
  detachInterrupt(digitalPinToInterrupt(2));

  // use leds to signal mat on
  digitalWrite(ledlockPin, HIGH);
  digitalWrite(ledunlockPin, HIGH);
  digitalWrite(ledPin, HIGH);

  delay(1000);

  digitalWrite(ledlockPin, LOW);
  digitalWrite(ledunlockPin, LOW);
  digitalWrite(ledPin, LOW);
  
  idle_clock_time = millis();
}

//wake up function
void wakeUpNow()  //This is the code that runs when the interrupt button is pressed and interrupts are enabled
{
  Serial.println("\n\nwake\n\n");
  idle_clock_time = millis();
}


//----------------------------------------------------------------

void setup() {
  pinMode(buttonPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(lockPin, OUTPUT);
  pinMode(unlockPin, OUTPUT);
  pinMode(ledlockPin, OUTPUT);
  pinMode(ledunlockPin, OUTPUT);
  
  for(int i = 0; i < 6; i++){
    unlockList[i] = 0;
  }

  Serial.begin(9600);
  Serial.println("button press value\n");

  // set LED state to high to signla mat is on
  digitalWrite(ledlockPin, HIGH);
  digitalWrite(ledunlockPin, HIGH);
  digitalWrite(ledPin, HIGH);

  delay(500);

  digitalWrite(ledlockPin, LOW);
  digitalWrite(ledunlockPin, LOW);
  digitalWrite(ledPin, LOW);

}

void loop() {
  button_state = GPIOBUTTONDETECT();
  
  if (button_state == 2){
    if (lock_timer_start){
      button_press_value = millis() - lock_clock_time;
      Serial.println(button_press_value);
    }

      //lock code
      if (button_press_value >= 5000){
        Serial.println("\nLOCK\n");
        digitalWrite(lockPin, HIGH);
        digitalWrite(ledlockPin, HIGH);
        delay(3000);
        digitalWrite(lockPin, LOW);
        digitalWrite(ledlockPin, LOW);
        for(int i = 0; i < 6; i++){
          passwordEnterList[i] = 0;
        }
      }

      else {
        //if there are 6 digits, add new digit, remove earliest chosen digit
        //uses function pushEnterList
        if ((button_press_value >= 50) && (button_press_value <= 1000)) {
          digitalWrite(ledunlockPin, HIGH);
          delay(200);
          digitalWrite(ledunlockPin, LOW);
        }

        if ((button_press_value > 500) && (button_press_value <= 1500)) {
          digitalWrite(ledlockPin, HIGH);
          delay(200);
          digitalWrite(ledlockPin, LOW);
        }
        pushEnterList(button_press_value);
      }

      lock_timer_start = false;
      idle_clock_time = millis();
  }

  if (button_state == 1){
    lock_timer_start = true;
    lock_clock_time = millis();
    idle_clock_time = millis();
  }

  if (button_state == 0){
    if (millis() - idle_clock_time >= 15000){ //idle time before sleeping
      sleepNow();
    }
  }

  for(int i = 0; i < 6; i++){
    if (abs(passwordList[i] - passwordEnterList[i]) <= 500){ //changes error margin
      unlockList[i] = 1;
    }
  }

  if ((unlockList[0] == 1) && (unlockList[1] == 1) && (unlockList[2] == 1) && (unlockList[3] == 1) && (unlockList[4] == 1) && (unlockList[5] == 1)){
    Serial.println("\nUNLOCK\n");
    digitalWrite(unlockPin, HIGH);
    digitalWrite(ledunlockPin, HIGH);
    delay(3000);
    digitalWrite(unlockPin, LOW);
    digitalWrite(ledunlockPin, LOW);
    for(int i = 0; i < 6; i++){
      passwordEnterList[i] = 100000;
    for(int i = 0; i < 6; i++){
      unlockList[i] = 0;
    }
    }
  }

  //reset unlock list to be updated later
  for(int i = 0; i < 6; i++){
    unlockList[i] = 0;
  }
    
    delay(50);
}
