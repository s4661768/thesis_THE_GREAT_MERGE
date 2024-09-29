#include <ArduinoBLE.h>

// 01/01/2000,00:01:27.36,-21.97,-79.10,-10\r\n
// 01/01/2000,00:01:27.37,-32.71,-78.61,-99\r\n
// 01/01/2000,00:01:27.38,-20.51,-71.78,-99\r\n
// 01/01/2000,00:01:27.39,-32.71,-68.36,-10\r\n
// 01/01/2000,00:01:27.40,-33.69,-57.13,-10\r\n
// 01/01/2000,00:01:27.41,-25.88,-63.48,-99\r\n
// 01/01/2000,00:01:27.42,-39.06,-64.94,-10\r\n
// 01/01/2000,00:01:27.43,-28.81,-62.99,-99\r\n
// 01/01/2000,00:01:27.44,-25.88,-72.75,-99\r\n
// 01/01/2000,00:01:27.45,-27.83,-48.34,-10\r\n
// 01/01/2000,00:01:27.46,-15.14,-74.22,-10\r\n
// 01/01/2000,00:01:27.47,-18.07,-59.08,-10\r\n
// 01/01/2000,00:01:27.48,-16.60,-70.80,-10\r\n
// 01/01/2000,00:01:27.49,-34.18,-64.45,-10\r\n
// 01/01/2000,00:01:27.50,-28.32,-72.27,-99\r\n
// 01/01/2000,00:01:27.51,-22.46,-59.57,-10\r\n
// 01/01/2000,00:01:27.52,-19.04,-61.04,-10\r\n
// 01/01/2000,00:01:27.53,-25.88,-76.17,-10\r\n
// 01/01/2000,00:01:27.54,-26.86,-61.04,-10\r\n
// 01/01/2000,00:01:27.55,-27.83,-66.89,-10\r\n
// 01/01/2000,00:01:27.56,-28.81,-65.43,-10\r\n
// 01/01/2000,00:01:27.57,-27.83,-67.38,-10\r\n
// 01/01/2000,00:01:27.58,-18.55,-73.73,-98\r\n
// 01/01/2000,00:01:27.59,-27.34,-69.34,-99\r\n
#define STRING_SIZE 1024
/* WMORE Service UUID */
const char* wmoreStringServiceUuid = "18ee1516-016b-4bec-ad96-bcb96d166e99";

/* WMORE String Characterstics */
const char* wmoreString1CharUuid = "18ee1516-016b-4bec-ad96-bcb96d166e9a";

BLEService wmoreStringService(wmoreStringServiceUuid);
BLEStringCharacteristic wmoreString1Char(wmoreString1CharUuid, BLERead | BLEBroadcast, STRING_SIZE);

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

      // wmoreString1Char.writeValue(my_string);
      // wmoreString1Char.writeValue("This is my string I hope the whole thing sends\r\nThis is another 50 chars totalling 100 chars !\r\n\r\n");
      // wmoreString1Char.writeValue("01/01/2000,00:01:27.36,-21.97,-79.10,-10\r\n\
      //                               01/01/2000,00:01:27.37,-32.71,-78.61,-99\r\n\
      //                               01/01/2000,00:01:27.38,-20.51,-71.78,-99\r\n\
      //                               01/01/2000,00:01:27.39,-32.71,-68.36,-10\r\n\
      //                               01/01/2000,00:01:27.40,-33.69,-57.13,-10\r\n\
      //                               01/01/2000,00:01:27.41,-25.88,-63.48,-99\r\n\
      //                               01/01/2000,00:01:27.42,-39.06,-64.94,-10\r\n\
      //                               01/01/2000,00:01:27.43,-28.81,-62.99,-99\r\n\
      //                               01/01/2000,00:01:27.44,-25.88,-72.75,-99\r\n\
      //                               01/01/2000,00:01:27.45,-27.83,-48.34,-10\r\n\
      //                               01/01/2000,00:01:27.46,-15.14,-74.22,-10\r\n\
      //                               01/01/2000,00:01:27.47,-18.07,-59.08,-10\r\n\
      //                               01/01/2000,00:01:27.48,-16.60,-70.80,-10\r\n\
      //                               01/01/2000,00:01:27.49,-34.18,-64.45,-10\r\n\
      //                               01/01/2000,00:01:27.50,-28.32,-72.27,-99\r\n\
      //                               01/01/2000,00:01:27.51,-22.46,-59.57,-10\r\n\
      //                               01/01/2000,00:01:27.52,-19.04,-61.04,-10\r\n\
      //                               01/01/2000,00:01:27.53,-25.88,-76.17,-10\r\n\
      //                               01/01/2000,00:01:27.54,-26.86,-61.04,-10\r\n\
      //                               01/01/2000,00:01:27.55,-27.83,-66.89,-10\r\n\
      //                               01/01/2000,00:01:27.56,-28.81,-65.43,-10\r\n\
      //                               01/01/2000,00:01:27.57,-27.83,-67.38,-10\r\n\
      //                               01/01/2000,00:01:27.58,-18.55,-73.73,-98\r\n\
      //                               01/01/2000,00:01:27.59,-27.34,-69.34,-99\r\n\
      //                               "
      //                             );
      wmoreString1Char.writeValue("01/01/2000,00:01:27.36,-21.97,-79.10,-1001/01/2000,00:01:27.37,-32.71,-78.61,-9901/01/2000,00:01:27.38,-20.51,-71.78,-9901/01/2000,00:01:27.39,-32.71,-68.36,-1001/01/2000,00:01:27.40,-33.69,-57.13,-1001/01/2000,00:01:27.41,-25.88,-63.48,-9901/01/2000,00:01:27.42,-39.06,-64.94,-1001/01/2000,00:01:27.43,-28.81,-62.99,-9901/01/2000,00:01:27.44,-25.88,-72.75,-9901/01/2000,00:01:27.45,-27.83,-48.34,-1001/01/2000,00:01:27.46,-15.14,-74.22,-1001/01/2000,00:01:27.47,-18.07,-59.08,-1001/01/2000,00:01:27.48,-16.60,-70.80,-1001/01/2000,00:01:27.49,-34.18,-64.45,-1001/01/2000,00:01:27.50,-28.32,-72.27,-9901/01/2000,00:01:27.51,-22.46,-59.57,-1001/01/2000,00:01:27.52,-19.04,-61.04,-1001/01/2000,00:01:27.53,-25.88,-76.17,-1001/01/2000,00:01:27.54,-26.86,-61.04,-1001/01/2000,00:01:27.55,-27.83,-66.89,-1001/01/2000,00:01:27.56,-28.81,-65.43,-1001/01/2000,00:01:27.57,-27.83,-67.38,-1001/01/2000,00:01:27.58,-18.55,-73.73,-9801/01/2000,00:01:27.59,-27.34,-69.34,-99")
      ;delay(1000);
    }
  }
}
