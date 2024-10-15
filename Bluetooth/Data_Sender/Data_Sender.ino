#include <ArduinoBLE.h>


#define STRING_SIZE 512
/* WMORE Service UUID */
const char* wmoreStringServiceUuid = "18ee1516-016b-4bec-ad96-bcb96d166e99";

/* WMORE String Send Characterstics */
const char* wmoreString1CharUuid = "18ee1516-016b-4bec-ad96-bcb96d166e9a";

/* WMORE RTC Receive Characterstics */
// const char* wmoreRTCRecvCharUuid = "18ee1516-016b-4bec-ad96-bcb96d166e9b";

BLEService wmoreStringService(wmoreStringServiceUuid);
BLEStringCharacteristic wmoreString1Char(wmoreString1CharUuid, BLERead | BLEBroadcast, STRING_SIZE);
// BLEIntCharacteristic wmoreRTCRecvChar(wmoreRTCRecvCharUuid, BLEWrite | BLEBroadcast);

// Advertising parameters should have a global scope. Do NOT define them in 'setup' or in 'loop'
const uint8_t completeRawAdvertisingData[] = {0x02,0x01,0x06,0x09,0xff,0x01,0x01,0x00,0x01,0x02,0x03,0x04,0x05};

// char my_string[STRING_SIZE] = {'\0'};
void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!BLE.begin()) {
    Serial.println("failed to initialize BLE!");
    while (1);
  }
  
  BLE.setAdvertisedService(wmoreStringService);
  wmoreStringService.addCharacteristic(wmoreString1Char);
  // wmoreStringService.addCharacteristic(wmoreRTCRecvChar);

  


  BLE.addService(wmoreStringService);

  // wmoreString1Char.writeValue(my_string);
  wmoreString1Char.writeValue("This is my string I hope the whole thing sends\r\n");

  // Build advertising data packet
  BLEAdvertisingData advData;
  // If a packet has a raw data parameter, then all the other parameters of the packet will be ignored
  advData.setRawData(completeRawAdvertisingData, sizeof(completeRawAdvertisingData));  
  // Copy set parameters in the actual advertising packet
  BLE.setAdvertisingData(advData);

  // Build scan response data packet
  BLEAdvertisingData scanData;
  scanData.setLocalName("WMORE Test scanString Dev0");
  // Copy set parameters in the actual scan response packet
  BLE.setScanResponseData(scanData);
  
  BLE.advertise();

  Serial.println("advertising ...");
}

void loop() {
  // BLE.poll();
  

  BLEDevice central = BLE.central();

  Serial.println("- Discovering Central Device");

  delay(1000);

  if (central) {
    Serial.printf("Connected to: %s\r\n", central.deviceName());
    
    while (central.connected()) {
      // if (wmoreRTCRecvChar.written()) {
      //   Serial.print("Recvd RTC Value\r\n");
      //   int num = wmoreRTCRecvChar.value();
      //   Serial.printf("RTC Value is: %d\r\n");
      // } 
      // 7 bytes
      // wmoreString1Char.writeValue("Hello\r\n");
      //512 bytes
      wmoreString1Char.writeValue("01/01/2000,00:01:27.36,-21.97,-79.10,-1001/01/2000,00:01:27.37,-32.71,-78.61,-9901/01/2000,00:01:27.38,-20.51,-71.78,-9901/01/2000,00:01:27.39,-32.71,-68.36,-1001/01/2000,00:01:27.40,-33.69,-57.13,-1001/01/2000,00:01:27.41,-25.88,-63.48,-9901/01/2000,00:01:27.42,-39.06,-64.94,-1001/01/2000,00:01:27.43,-28.81,-62.99,-9901/01/2000,00:01:27.44,-25.88,-72.75,-9901/01/2000,00:01:27.45,-27.83,-48.34,-1001/01/2000,00:01:27.46,-15.14,-74.22,-1001/01/2000,00:01:27.47,-18.07,-59.08,-1001/01/2000,00:01:27.48,-16.60,-7");
      
    }
  }
}