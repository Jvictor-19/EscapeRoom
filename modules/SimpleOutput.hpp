#ifndef SIMPLE_OUTPUT_H
#define SIMPLE_OUTPUT_H
#include "Arduino.h"

class SimpleOutput {
private:
  const uint8_t _out_pin;

public:
  SimpleOutput(uint8_t out_pin);
  void begin();
  
  void set();
  void clear();
  void switchState();

  bool state();
};

#endif
