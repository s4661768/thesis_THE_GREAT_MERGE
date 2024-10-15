import asyncio
import time
from bleak import BleakScanner
from bleak import BleakClient
import os

global recv
recv = 0
MSG_LEN = 512
START_MESSAGE = 4294967295
async def read_from_client(client, uuid) -> str:
    string = None
    string = await client.read_gatt_char(uuid)
    global recv 
    recv += 1
    return string

async def write_to_client(client: BleakClient, uuid, value: int, response=False):
    
    value = await client.write_gatt_char(uuid, value.to_bytes(4, 'little'), response)
    return value
    

async def main():
    # Look for WMORE devices
    wmore_dev = None
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == "WMORE Test scanString Dev0":
            wmore_dev = d
            print()
            print(f"WMORE Dev Found: {d.address} --- {d.name}")
            print()
            break
    if wmore_dev is None:
        print("NO WMORE DEVICES FOUND")
        return
    # Connecting to found device
    async with BleakClient(wmore_dev.address) as client:
        print("Connecting to device")
        print()
        string_service = None
        string_char_1 = None

        print("Device Services --------------------------------")
        for service in client.services:
            print(f"Service: {service}")
            

            try:

                for characteristic in service.characteristics:
                    print("Device Characteristics -------------------------")
                    print(f"Characteristic: {characteristic}")

                    string_char_1 = service.get_characteristic("18ee1516-016b-4bec-ad96-bcb96d166e9a")
                    if string_char_1 is not None:
                        print("FOUND THE RIGHT SERVICE AND CHARACTERISTIC")
                        print(type(string_char_1))
                        string_service = service
                        rtc_send_char = service.get_characteristic("18ee1516-016b-4bec-ad96-bcb96d166e9b")
                        break

                    else:
                        print("CHARACTERISTIC IS INCORRECT")
                        continue

                    
            except Exception as e:
                print(f"Error -------------------------\r\n{e}")
                exit(1)

            if string_service is None or string_char_1 is None:
                print("Service and Characteristics NOT found (major w)")
                print("Continuing loop")
                continue
            else:
                break

        if string_service is None or string_char_1 is None:
            print("NOTHING FOUND\r\nPROGRAM EXITTING...")
            value = await client.disconnect()
            exit(0)

        print("\r\n\r\n\r\n")
        print("Service and Characterstics found (major w)")
        print("-----------------------------------------------")

        print(f"String Service: {string_service}\r\n")
        print(f"String Characteristic 1: {string_char_1}\r\n")
        print(f"RTC Send Characteristic 1: {rtc_send_char}\r\n")

        await write_to_client(client, rtc_send_char, START_MESSAGE, response=True)
        # value = await client.write_gatt_char(rtc_send_char, START_MESSAGE.to_bytes(4, 'little'), response=True)
    
        
        time.sleep(1)
        os.system('cls')



        # Reading from Characteristics
        start_time = time.time()
        
        while True:
            global recv

            if recv > 0:

                print(F"TIME: {time.time() - start_time}")
                print(F"BITS PER SECOND: {(recv * MSG_LEN * 8) / (time.time() - start_time)}")
                print(F"BYTES PER SECOND: {(recv * MSG_LEN) / (time.time() - start_time)}")
                print()
                      
            

            # Read from client


            # string_1 = await client.read_gatt_char(string_char_1)
            string_1 = await read_from_client(client, string_char_1)

            if string_1 is not None:
                # print(f"String 1: {string_1.decode('utf8')}") # Not printing just to save time
                
                string_1 = None
            else:
                print(f"String 1: ~NO DATA~")       

    value = await client.disconnect()

    print(f"Disconnected from device {value}")

asyncio.run(main())