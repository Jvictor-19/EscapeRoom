#include <SPI.h>
#include <MFRC522.h>
#include <SimpleOutput.hpp>

constexpr unsigned long SERIAL_NUMBER = 9600;
constexpr uint8_t       N_READERS = 2;
constexpr uint8_t       RESET_PIN = 3;
constexpr uint8_t       SDA_PINS[N_READERS] = { 2, 4 };
constexpr uint8_t       LOCK_PIN = 5;
constexpr uint8_t       UIDS[N_READERS][4] = {
	{ 0xFA, 0x97, 0xED, 0x05 },
	{ 0x6E, 0x2D, 0x91, 0x05 }
};

SimpleOutput lock(LOCK_PIN);
MFRC522 readers[N_READERS];
bool areTagsPresent;

void printUID(const MFRC522& reader) {
	Serial.print("UID:");
	for(uint8_t i = 0; i < reader.uid.size; i++) {
		Serial.print(reader.uid.uidByte[i] < 0x10 ? " 0" : " ");
		Serial.print(reader.uid.uidByte[i], HEX);
	}
	Serial.print('\n');
}

bool sameUID(const uint8_t *UID_A, const uint8_t *UID_B) {
	return memcmp(UID_A, UID_B, 4) == 0;
}

void setup() {
	Serial.begin(SERIAL_NUMBER);
	SPI.begin();
	lock.begin();

	for(uint8_t i = 0; i < N_READERS; i++) {
		readers[i].PCD_Init(SDA_PINS[i], RESET_PIN);
		readers[i].PCD_SetAntennaGain(MFRC522::RxGain_max);
	}

	delay(4);
}

void loop() {
	areTagsPresent = true;

	for(uint8_t i = 0; i < N_READERS; i++) {
		if(!readers[i].PICC_IsNewCardPresent()) {
			areTagsPresent = false;
			break;
		}
		readers[i].PICC_ReadCardSerial();
		readers[i].PICC_IsNewCardPresent();

		if(!sameUID(readers[i].uid.uidByte, UIDS[i])) {
			areTagsPresent = false;
			break;
		}
	}

	if(areTagsPresent) {
		lock.set();
		delay(10000);
	}
	else {
		lock.clear();
	}
}