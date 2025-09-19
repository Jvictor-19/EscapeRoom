#include "ChestLock.hpp"

const uint8_t sla[] = { 5, 7, 8, 13 };
ChestLock<4> chest(sla, 4);

void setup() {
  chest.begin();
}

void loop() {
  chest.invTryUnlock();
}  
