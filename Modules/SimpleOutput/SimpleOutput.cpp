#include "Arduino.h"
#include "SimpleOutput.hpp"

SimpleOutput::SimpleOutput(uint8_t out_pin) 
: _out_pin(out_pin)
{}

void SimpleOutput::begin() {
  pinMode(_out_pin, OUTPUT);
  digitalWrite(_out_pin, LOW);
}

void SimpleOutput::set() {
  digitalWrite(_out_pin, HIGH);
}

void SimpleOutput::clear() {
  digitalWrite(_out_pin, LOW);
}

void SimpleOutput::switchState() {
  digitalWrite(_out_pin, !digitalRead(_out_pin));
}

bool SimpleOutput::state() {
  return digitalRead(_out_pin);
}
