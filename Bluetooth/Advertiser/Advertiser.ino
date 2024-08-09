#include <ArduinoBLE.h>


const char* wmoreServiceUuid = "18ee1516-016b-4bec-ad96-bcb96d166e99";
const char* wmoreDataSendCharacteristiceUuid = "18ee1516-016b-4bec-ad96-bcb96d166e9a";
const char* wmoreDataRecvCharacteristiceUuid = "18ee1516-016b-4bec-ad96-bcb96d166e9b";

BLEService wmoreStreamingService(wmoreServiceUuid);
BLEIntCharacteristic wmoreSendDataCharacteristic(wmoreDataSendCharacteristiceUuid, BLERead | BLEBroadcast);
BLEIntCharacteristic wmoreRecvDataCharacteristic(wmoreDataRecvCharacteristiceUuid, BLEWrite | BLEBroadcast);

// Advertising parameters should have a global scope. Do NOT define them in 'setup' or in 'loop'
const uint8_t completeRawAdvertisingData[] = {0x02,0x01,0x06,0x09,0xff,0x01,0x01,0x00,0x01,0x02,0x03,0x04,0x05};   

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!BLE.begin()) {
    Serial.println("failed to initialize BLE!");
    while (1);
  }
  
  BLE.setAdvertisedService(wmoreStreamingService);
  wmoreStreamingService.addCharacteristic(wmoreSendDataCharacteristic);
  wmoreStreamingService.addCharacteristic(wmoreRecvDataCharacteristic);
  BLE.addService(wmoreStreamingService);

  wmoreSendDataCharacteristic.writeValue(1);

  // Build advertising data packet
  BLEAdvertisingData advData;
  // If a packet has a raw data parameter, then all the other parameters of the packet will be ignored
  advData.setRawData(completeRawAdvertisingData, sizeof(completeRawAdvertisingData));  
  // Copy set parameters in the actual advertising packet
  BLE.setAdvertisingData(advData);

  // Build scan response data packet
  BLEAdvertisingData scanData;
  scanData.setLocalName("WMORE Test scanData");
  // Copy set parameters in the actual scan response packet
  BLE.setScanResponseData(scanData);
  
  BLE.advertise();

  Serial.println("advertising ...");
}

void loop() {
  // BLE.poll();
  BLEDevice central = BLE.central();
  Serial.println("- Discovering Central Device");
  delay(500);

  if (central) {
    Serial.printf("Connected to: %s\r\n", central.deviceName());

    while (central.connected()) {
      if (wmoreRecvDataCharacteristic.written()) {
        int new_num = wmoreRecvDataCharacteristic.value();
        wmoreSendDataCharacteristic.writeValue(new_num);
        Serial.printf("Recved: %d\r\n", new_num);
        delay(10);
      }
    }
  }

}