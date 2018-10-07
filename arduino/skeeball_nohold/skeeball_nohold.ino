#include <TimerOne.h>

unsigned long buttons = 0;
unsigned long pressed = 0;
char btn;

#define set(x) \
  buttons |= 1L << x;
#define clr(x) \
  buttons &= ~(1L << x);
#define tog(x) \
  buttons ^= 1L << x;
#define chk(x) \
  (pressed >> x) & 1L



void buttonHandle() {
  for (btn = 2; btn <= 19; btn++) {
    if(digitalRead(btn)) {
      clr(btn);
    } else {
      set(btn);
    }
  }
  pressed |= (buttons);
}

void sendButtons() {
  Serial.write((char *)&pressed,sizeof(pressed));
  pressed = 0;
}

void setup() {
  int x;
  for (x = 2; x <= 19; x++){
    pinMode(x,INPUT_PULLUP);
  }
  Timer1.initialize(20000);
  Timer1.attachInterrupt(buttonHandle);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
     char cmd = Serial.read();
     if (cmd == 'B') {
       sendButtons();
     }
  }
}
