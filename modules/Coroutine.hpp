#ifndef COROUTINE
#define COROUTINE

#include "Arduino.h"

class Coroutine {
private:
  void (*_func)(void);
  unsigned long _last_call;
public:
  unsigned long cooldown;

  Coroutine(void (*func)(void), unsigned long cooldown);

  void operator()(void);
};

#endif 
