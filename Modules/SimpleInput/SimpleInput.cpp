#include "Arduino.h"
#include "SimpleInput.hpp"

SimpleInput::SimpleInput(uint8_t in_pin)
: _in_pin(in_pin) 
{}

void SimpleInput::begin() {
  pinMode(_in_pin, INPUT_PULLUP);
}

bool SimpleInput::read() {
  return digitalRead(_in_pin);
}