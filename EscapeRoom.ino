#include <SPI.h>
#include <MFRC522.h>
#include <SimpleOutput.hpp>

// Parâmetros do programa
constexpr unsigned long SERIAL_NUMBER = 9600;                // Portal serial para comunicação
constexpr uint8_t       N_READERS = 2;                       // Número de leitores RFC522 no circuito
constexpr uint8_t       RESET_PIN = 3;                       // Conexão rst do leitor, um pino compartilhado para todos os leitores
constexpr uint8_t       SDA_PINS[N_READERS] = { 2, 4 };      // Conexões SDA/SS dos leitores, um pino para cada leitor
constexpr uint8_t       LOCK_PIN = 5;                        // Pino de saída 
constexpr unsigned long UNLOCKED_TIME = 30000;               // Tempo que a saída fica ativa antes de verificar novamente
constexpr uint8_t       UIDS[N_READERS][4] = {               // UID que cada leitor estará procurando
	// Na função loop tem comentários explicando como ler os UIDs usando este mesmo código-fonte
	// Aqui estão as UIDs dos meus cartões
	{ 0xFA, 0x97, 0xED, 0x05 },
	{ 0x6E, 0x2D, 0x91, 0x05 }
};

// Variáveis globais
SimpleOutput lock(LOCK_PIN);
MFRC522      readers[N_READERS];
bool         are_tags_present; 

// Função para debug
void printUID(const MFRC522& reader) {
	Serial.print("UID:");
	for(uint8_t i = 0; i < reader.uid.size; i++) {
		Serial.print(reader.uid.uidByte[i] < 0x10 ? " 0" : " ");
		Serial.print(reader.uid.uidByte[i], HEX);
	}
	Serial.print('\n');
}

// Compara se dois UIDs são os mesmos
bool sameUID(const uint8_t *UID_A, const uint8_t *UID_B) {
	return memcmp(UID_A, UID_B, 4) == 0;
}

void setup() {
	Serial.begin(SERIAL_NUMBER);
	SPI.begin();
	lock.begin();

	// Inicializando cada um dos leitores
	for(uint8_t i = 0; i < N_READERS; i++) {
		readers[i].PCD_Init(SDA_PINS[i], RESET_PIN);
		readers[i].PCD_SetAntennaGain(MFRC522::RxGain_max); // Não parece fazer muita diferença
	}

	delay(4); // Delay opicional. Serve para microcontroladores especificos
}

void loop() {
	are_tags_present = true;

	for(uint8_t i = 0; i < N_READERS; i++) {
		if(!readers[i].PICC_IsNewCardPresent()) {
			are_tags_present = false;
			break;
		}
		readers[i].PICC_ReadCardSerial();

		// Descomente a linha imediatamente abaixo para habilitar o print dos cartões que se aproximam, qualquer leitor serve
		// printUID(readers[i]);

		// Isso é uma gambiarra, mas a outra forma de ler continuamente é bem mais complicada
		// https://github.com/miguelbalboa/rfid/wiki/Useful-code-snippets
		readers[i].PICC_IsNewCardPresent();

		if(!sameUID(readers[i].uid.uidByte, UIDS[i])) {
			are_tags_present = false;
			break;
		}
	}

	if(are_tags_present) {
		lock.set();
		delay(UNLOCKED_TIME);
	}
	else {
		lock.clear();
	}
}