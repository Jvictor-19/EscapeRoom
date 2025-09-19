#ifndef SIMPLE_INPUT
#define SIMPLE_INPUT

#include "Arduino.h"

class SimpleInput {
private:
  const uint8_t _in_pin;

public:
  SimpleInput(uint8_t in_pin);
  void begin();

  bool read();
};

#endif