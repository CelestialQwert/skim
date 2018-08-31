#include <TimerOne.h>

unsigned int buttons = 0;
unsigned int pressed = 0;
unsigned int held = 0;
unsigned char held_time[16] = "";

#define set(x) \
  buttons |= 1 << x;
#define clr(x) \
  buttons &= ~(1 << x);
#define tog(x) \
  buttons ^= 1 << x;
#define chk(x) \
  (pressed >> x) & 1

char btn;

void buttonHandle() {
  for (btn = 2; btn < 13; btn++) {
    if(digitalRead(btn)) {
      clr(btn-2);
      held_time[btn-2] = 0;
    } else {
      set(btn-2);
      if (held_time[btn-2] < 250) {
        held_time[btn-2] += 1;
      }
    }
  }
  pressed |= ( buttons & ~held);
  held = buttons;
}

void sendButtons() {
  Serial.write((char *)&pressed,sizeof(pressed));
  pressed = 0;
  Serial.write(held_time,sizeof(held_time));
}

void setup() {
  int x;
  for (x = 2; x<13; x++)
    pinMode(x,INPUT_PULLUP);
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
