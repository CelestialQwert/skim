unsigned long buttons = 0;

#define set(x) \
  buttons |= 1L << x;
#define clr(x) \
  buttons &= ~(1L << x);
#define tog(x) \
  buttons ^= 1L << x;
#define chk(x) \
  (pressed >> x) & 1L

char btn;

void buttonHandle() {
  for (btn = 2; btn <= 19; btn++) {
    if(digitalRead(btn)) {
      clr(btn);
    } else {
      set(btn);
    }
  }
}

void setup() {
  int x;
  for (x = 2; x <= 19; x++){
    pinMode(x,INPUT_PULLUP);
  }
  Serial.begin(9600);
}

void loop() {
  buttonHandle();
  Serial.write((char *)&buttons,sizeof(buttons));
  delay(50);
}
