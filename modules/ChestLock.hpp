#ifndef CHEST_LOCK
#define CHEST_LOCK

#include "Arduino.h"

template<uint8_t n_in_pins>
class ChestLock {
private:
  const uint8_t(& _in_pins)[n_in_pins];
  const uint8_t _out_pin;

public:
  ChestLock(const uint8_t(& in_pins)[n_in_pins], uint8_t out_pin);
  void begin() const;

  void tryUnlock() const;
  void invTryUnlock() const;

  bool locked() const;
  bool checkAllPins() const;
  bool invCheckAllPins() const;
  bool checkPin(uint8_t index) const;

  constexpr uint8_t inPinsSize() const;
};

template<uint8_t n_in_pins>
ChestLock<n_in_pins>::ChestLock(const uint8_t(& in_pins)[n_in_pins], uint8_t out_pin)
: _in_pins(in_pins), _out_pin(out_pin)
{}

template<uint8_t n_in_pins>
void ChestLock<n_in_pins>::begin() const {
  pinMode(_out_pin, OUTPUT);
  digitalWrite(_out_pin, HIGH);

  for(uint8_t i = 0; i < n_in_pins; i++) {
    pinMode(_in_pins[i], INPUT_PULLUP);
  }
}

template<uint8_t n_in_pins>
constexpr uint8_t ChestLock<n_in_pins>::inPinsSize() const {
  return n_in_pins;
}

template<uint8_t n_in_pins>
void ChestLock<n_in_pins>::tryUnlock() const {
  bool result = true;

  for(uint8_t i = 0; i < n_in_pins && result; i++) {
    result = result && digitalRead(_in_pins[i]);
  }

  digitalWrite(_out_pin, result);
}

template<uint8_t n_in_pins>
void ChestLock<n_in_pins>::invTryUnlock() const {
  bool result = true;

  for(uint8_t i = 0; i < n_in_pins && result; i++) {
    result = result && !digitalRead(_in_pins[i]);
  }

  digitalWrite(_out_pin, result);
}

template<uint8_t n_in_pins>
bool ChestLock<n_in_pins>::locked() const {
  return digitalRead(_out_pin);
}

template<uint8_t n_in_pins>
bool ChestLock<n_in_pins>::checkAllPins() const {
  bool result = true;

  for(uint8_t i = 0; i < n_in_pins && result; i++) {
    result = result && digitalRead(_in_pins[i]);
  }

  return result;
}

template<uint8_t n_in_pins>
bool ChestLock<n_in_pins>::invCheckAllPins() const {
  bool result = true;

  for(uint8_t i = 0; i < n_in_pins && result; i++) {
    result = result && !digitalRead(_in_pins[i]);
  }

  return result;
}

template<uint8_t n_in_pins>
bool ChestLock<n_in_pins>::checkPin(uint8_t index) const {
  return digitalRead(_in_pins[index]);
}

#endif