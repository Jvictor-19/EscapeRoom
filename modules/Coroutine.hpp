// Wrapper que adiciona cooldown a funções, não permitindo a chamada enquanto esse cooldown não estiver zerado, abrindo a possibilidade para ciclos e delays não bloqueantes

#ifndef COROUTINE
#define COROUTINE

#include "Arduino.h"

class Coroutine {
private:
  // Ponteiro da função, é necessário que ela não tenha parâmetro e que retorne void, uma subrotina
  void (*_func)(void);

  // Armazena os millisegundos do tempo que foi chamada pela última vez
  unsigned long _last_call;
public:
  // Armazena o tempo, em milissegundos, que a função estará desabilitada
  unsigned long cooldown;

  Coroutine(void (*func)(void), unsigned long cooldown);

  // Açúcar sintático para chamada do ponteiro de função
  void operator()(void);
};

#endif 
