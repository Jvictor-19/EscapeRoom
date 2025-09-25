// Wrapper idiomático para funções padrões do Arduino voltado a pinos de output

#ifndef SIMPLE_OUTPUT_H
#define SIMPLE_OUTPUT_H
#include "Arduino.h"

class SimpleOutput {
private:
  // Armazena o pino de saída
  const uint8_t _out_pin;

public:
  // Inicialização dupla
  // Chame o construtor padrão e depois termine a inicialização com o .begin()
  SimpleOutput(uint8_t out_pin);
  void begin();
  
  // Saída emite 1
  void set();
  
  // Saída emite 0
  void clear();

  // Inverte o estado atual
  void switchState();

  // Lê o estado atual e retorna-o
  bool state();
};

#endif
