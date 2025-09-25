#include "Coroutine.hpp"

Coroutine::Coroutine(void (*func)(void), unsigned long cooldown)
: _func(func), cooldown(cooldown) {
  _last_call = 0;
}

void Coroutine::operator()() {
  unsigned long current = millis();

  if(current - _last_call >= cooldown) {
    _func();
    _last_call = current;
  }
}