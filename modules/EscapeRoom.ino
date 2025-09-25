#include "Coroutine.hpp"
#include "SimpleOutput.hpp"

SimpleOutput a(10);

void teste() {
  a.switchState();
}

Coroutine frangles(teste, 1000);

void setup() {
  a.begin();
  pinMode(2, OUTPUT);
}

void loop() {
  frangles();
}