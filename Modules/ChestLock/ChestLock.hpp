// Módulo que adiciona uma única classe chamada ChestLock
// ChestLock serve como abstração de um dos objetos do Escape Room, o baú

#ifndef CHEST_LOCK
#define CHEST_LOCK

#include "Arduino.h"

// Template tem como argumento a quantidade de pinos de entrada que servirão como tranca
template<uint8_t n_in_pins>
class ChestLock {
private:
  // Array que armazena os índices dos pinos de entrada
  const uint8_t(& _in_pins)[n_in_pins];
  // Armazena o índice pino de saída
  const uint8_t _out_pin;

public:
  // Inicialização dupla
  // Chame o construtor padrão e depois termine a inicialização com o .begin()
  ChestLock(const uint8_t(& in_pins)[n_in_pins], uint8_t out_pin);
  void begin() const;

  // Ambas as funções escrevem no pino de saída o resultado das seguintes equações lógica, respectivamente
  void tryUnlock() const; // out_pin = _in_pins[0] & _in_pins[1] & _in_pins[2] & ... & _in_pins[n_in_pins - 1]
  void invTryUnlock() const; // out_pin = ~_in_pins[0] & ~_in_pins[1] & ~_in_pins[2] & ... & ~_in_pins[n_in_pins - 1]

  // Retorna o estado do pino de saída
  bool locked() const;

  // Fazem a mesma checagem das funções try acima, no entanto, não muda o estado de nenhum pino, retornando a função lógica
  bool checkAllPins() const;
  bool invCheckAllPins() const;

  // Checa um único pino baseado no seu índice na array _in_pins 
  bool checkPin(uint8_t index) const;

  // Retorna a quantidade de pinos de entrada
  constexpr uint8_t inPinsSize() const;
};

/*
 * As implementações tem de ficar no .hpp devido ao fato da classe ser template
 */

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