unsigned long hold_time = 0;
unsigned long unhold_time = 0;
unsigned long real_unhold_time = 0;
unsigned long press_time = 0;
unsigned long unpress_time = 0;

bool held;
int btn;

void setup(){
  btn = 8;
  pinMode(btn,INPUT_PULLUP);
  Serial.begin(9600);
  held = false;
}
void loop(){
  if (digitalRead(btn) == LOW && !held)  {
    held = true;
    press_time = millis();
    unhold_time = millis() - unpress_time;
    if (unhold_time > 2) {
      real_unhold_time = unhold_time;
    }
  }
  if (digitalRead(btn) == HIGH && held){
    held = false;
    unpress_time = millis();
    hold_time = millis() - press_time;
    if (hold_time > 2){
      Serial.print("Held ");
      Serial.print(hold_time);
      Serial.print(" ms, unheld ");
      Serial.print(real_unhold_time);
      Serial.print(" ms, total ");
      Serial.print(real_unhold_time+hold_time);
      Serial.println(" ms");
    }
  }
}
