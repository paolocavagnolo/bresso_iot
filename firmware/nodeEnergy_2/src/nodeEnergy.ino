// FIRMWARE CARICATO IL 23-9-2016
// QUADRO ELETTRICO PRINCIPALE - ALL'INGRESSO

#include <PinChangeInt.h>
#include <RFM69.h>         //get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPI.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <SPIFlash.h>      //get it here: https://www.github.com/lowpowerlab/spiflash
#include <avr/wdt.h>
#include <avr/io.h>
#include <avr/wdt.h>

#define PIN_A 14  // the pin we are interested in
#define PIN_B 15  // the pin we are interested in
#define PIN_C 16  // the pin we are interested in
volatile byte tA = 0;  // a counter to see how many times the pin has changed
volatile byte tB = 0;  // a counter to see how many times the pin has changed
volatile byte tC = 0;  // a counter to see how many times the pin has changed
unsigned long ttA = 0;
unsigned long ttB = 0;
unsigned long ttC = 0;
unsigned long ttA_o = 0;
unsigned long ttB_o = 0;
unsigned long ttC_o = 0;
byte ttA_b[4];
byte ttB_b[4];
byte ttC_b[4];

#define Reset_AVR() wdt_enable(WDTO_30MS); while(1) {}

#define NODEID      2       // node ID used for this unit
#define NETWORKID   90
#define GATEWAYID   1

#define FREQUENCY   RF69_433MHZ

#define IS_RFM69HW  //uncomment only for RFM69HW! Leave out if you have RFM69W!
#define SERIAL_BAUD 115200
#define ACK_TIME    30  // # of ms to wait for an ack
#define ENCRYPTKEY "alessandro123456" //(16 bytes of your choice - keep the same on all encrypted nodes)

#define LED           9 // Moteinos hsave LEDs on D9
#define FLASH_SS      8 // and FLASH SS on D8

#define COUNT_TICK 10

byte sendSize = 6;
boolean requestACK = false;

RFM69 radio;
char input = 0;
long lastPeriod = -1;

SPIFlash flash(FLASH_SS, 0xEF30); //EF30 for windbond 4mbit flash

bool fA, fB, fC;

void setup() {
  Serial.begin(9600);

  pinMode(LED, OUTPUT);

  pinMode(PIN_A, INPUT);     //set the pin to input
  digitalWrite(PIN_A, HIGH); //use the internal pullup resistor
  pinMode(PIN_B, INPUT);     //set the pin to input
  digitalWrite(PIN_B, HIGH); //use the internal pullup resistor
  pinMode(PIN_C, INPUT);     //set the pin to input
  digitalWrite(PIN_C, HIGH); //use the internal pullup resistor

  PCintPort::attachInterrupt(PIN_A, burpcount_a, RISING); // attach a PinChange Interrupt to our pin on the rising edge
  PCintPort::attachInterrupt(PIN_B, burpcount_b, RISING); // attach a PinChange Interrupt to our pin on the rising edge
  PCintPort::attachInterrupt(PIN_C, burpcount_c, RISING); // attach a PinChange Interrupt to our pin on the rising edge
  // (RISING, FALLING and CHANGE all work with this library)
  // and execute the function burpcount when that pin changes

  radio.initialize(FREQUENCY, NODEID, NETWORKID);
  radio.encrypt(ENCRYPTKEY); //OPTIONAL
#ifdef IS_RFM69HW
  radio.setHighPower(); //only for RFM69HW!
#endif

  flash.initialize();

}

char message[6];
long timeoutMAX = 60000000;

void loop() {

  if (radio.receiveDone()) {
    if (radio.ACKRequested()) radio.sendACK();
  }

  if (tA >= 1) {
    ttA = millis();
    tA = tA - 1;

    Serial.print("ttA: ");
    Serial.print(ttA);
    Serial.print("\t");
    Serial.print("ttA_o: ");
    Serial.print(ttA_o);
    Serial.print("\t");
    Serial.print("diff: ");
    Serial.print((long)(ttA-ttA_o));
    Serial.println("\t");

    if ((long)(ttA-ttA_o) > 0) {
      float2Bytes(ttA-ttA_o, &ttA_b[0]);
    }
    else {
      //rollover!
      float2Bytes(((4294967296-ttA_o)+ttA), &ttA_b[0]);
    }

    ttA_o = ttA;

    message[0] = 'e';
    message[1] = 'a';
    message[2] = ttA_b[0];
    message[3] = ttA_b[1];
    message[4] = ttA_b[2];
    message[5] = ttA_b[3];
    radio.sendWithRetry(GATEWAYID, message, sendSize);
  }
  if (tB >= 1) {
    ttB = millis();
    tB = tB - 1;

    Serial.print("ttB: ");
    Serial.print(ttB);
    Serial.print("\t");
    Serial.print("ttB_o: ");
    Serial.print(ttB_o);
    Serial.print("\t");
    Serial.print("diff: ");
    Serial.print((long)(ttB-ttB_o));
    Serial.println("\t");

    if ((long)(ttB-ttB_o) > 0) {
      float2Bytes(ttB-ttB_o, &ttB_b[0]);
    }
    else {
      //rollover!
      float2Bytes(((4294967296-ttB_o)+ttB), &ttB_b[0]);
    }

    ttB_o = ttB;

    message[0] = 'e';
    message[1] = 'b';
    message[2] = ttB_b[0];
    message[3] = ttB_b[1];
    message[4] = ttB_b[2];
    message[5] = ttB_b[3];
    radio.sendWithRetry(GATEWAYID, message, sendSize);
  }
  if (tC >= 1) {
    ttC = millis();
    tC = tC - 1;

    Serial.print("ttC: ");
    Serial.print(ttC);
    Serial.print("\t");
    Serial.print("ttC_o: ");
    Serial.print(ttC_o);
    Serial.print("\t");
    Serial.print("diff: ");
    Serial.print((long)(ttC-ttC_o));
    Serial.println("\t");

    if ((long)(ttC-ttC_o) > 0) {
      float2Bytes(ttC-ttC_o, &ttC_b[0]);
    }
    else {
      //rollover!
      float2Bytes(((4294967296-ttC_o)+ttC), &ttC_b[0]);
    }

    ttC_o = ttC;

    message[0] = 'e';
    message[1] = 'c';
    message[2] = ttC_b[0];
    message[3] = ttC_b[1];
    message[4] = ttC_b[2];
    message[5] = ttC_b[3];
    radio.sendWithRetry(GATEWAYID, message, sendSize);
  }

  // end loop

}

void burpcount_a()
{
  tA++;
}
void burpcount_b()
{
  tB++;
}
void burpcount_c()
{
  tC++;
}

void float2Bytes(float val, byte* bytes_array) {
  // Create union of shared memory space
  union {
    float float_variable;
    byte temp_array[4];
  } u;
  // Overwite bytes of union with float variable
  u.float_variable = val;
  // Assign bytes to input array
  memcpy(bytes_array, u.temp_array, 4);
}

void long2Bytes(long val, byte* bytes_array) {
  // Create union of shared memory space
  union {
    long long_variable;
    byte temp_array[4];
  } u;
  // Overite bytes of union with float variable
  u.long_variable = val;
  // Assign bytes to input array
  memcpy(bytes_array, u.temp_array, 4);
}

float bytes2Float(byte* bytes_array) {
  float val;

  union {
    float fval;
    byte b[4];
  } u;

  u.b[0] = bytes_array[0];
  u.b[1] = bytes_array[1];
  u.b[2] = bytes_array[2];
  u.b[3] = bytes_array[3];

  val = u.fval;
  return val;
}
