// Wrapper idiomático para funções padrões do Arduino voltado a pinos de input

#ifndef SIMPLE_INPUT
#define SIMPLE_INPUT

#include "Arduino.h"

class SimpleInput {
private:
  // Armazena pino de entrada
  const uint8_t _in_pin;

public:
  // Inicialização dupla
  // Chame o construtor padrão e depois termine a inicialização com o .begin()
  SimpleInput(uint8_t in_pin);
  void begin();

  // Lê o valor da entrada
  bool read();
};

#endif