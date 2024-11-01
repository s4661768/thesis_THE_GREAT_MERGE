import asyncio
import time
from bleak import BleakScanner
from bleak import BleakClient
import os
# from MyPlotter import Simulation
import Parse
from threading import Thread
import keyboard
import pandas as pd

global recv
recv = 0
MSG_LEN = 42


RTC = 0
SYS_TIME = 1

global End 
End = False
global filename
filename = "./temp.csv"
global Data
Data = []


class Streaming_Client():
    def __init__(self, client_name, service, streaming_char):
        self.client_name = client_name
        self._device = None
        self.client = None
        self.service = service
        self.streaming_char = streaming_char

    def set_device(self, device):
        self._device = device
    
    def get_device(self):
        return self._device

    async def read_from_client(self) -> str:
        string = None
        string = await self.client.read_gatt_char(self.streaming_char)
        global recv 
        recv += 1
        return string
    
    def set_client(self, client):
        self.client = client

    def get_client(self) -> BleakClient:
        return self.client
        



async def find_device(dev_name: str):
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == dev_name:
            return d
    raise ValueError(f"Device '{dev_name}' not found")

async def main():
    d = None
    d = await find_device("WMORE Logger Streamer 0")
    print(d.name)
    streamer = Streaming_Client(d.name, "18ee1516-016b-4bec-a596-bcb96d160405", "18ee1516-016b-4bec-ad96-bcb96d160406")
    streamer.set_device(d)
    async with BleakClient(streamer.get_device().address) as c:
        streamer.set_client(c)
        print("Connected to device")
        
        try:
            
            for s in streamer.client.services:
                print(f"Services: {s}")

                for c in s.characteristics:
                    print(f"Characteristics: {c}")
            # d = []
            # t = threading.Thread(target=Simulation().run, args=(d,))
            # t.start()
            # sim = Simulation(filter_width=5)
            # start_time = time.time()
            
            global End, Data
            while True:
                string = await streamer.read_from_client()
                # delta = time.time() - start_time
                # print(F"MSGS/SEC: {recv / delta}\r\nTIME: {delta}\r\nBITS PER SECOND: {(recv * MSG_LEN * 8) / (delta)}\r\nBYTES PER SECOND: {(recv * MSG_LEN) / (delta)}")
                # print(F"BITS PER SECOND: {(recv * MSG_LEN * 8) / (time.time() - start_time)}")
                # print(F"BYTES PER SECOND: {(recv * MSG_LEN) / (time.time() - start_time)}")
                
                print(Parse.parse_time(string.decode('utf-8')))
                Data.append([Parse.parse_time(string.decode('utf-8')), time.time()])
                # print(f"Received String: {string.decode('utf-8')}")
            
                if End:
            
                    
                    print("Stopped listening...")
                    print("Writing to file now...")
                    print(Data)
                    # with open(temp_file, "a") as f:
                    #     for line in data:
                    #         f.writelines(str(line) + "\r\n")
                            
                        
                    # f.close()
                    global filename
                    df = pd.DataFrame(Data, columns=['RTC_TIME', 'SYS_TIME'])
                    df.to_csv(filename, index=False)
                    print("Writing complete... Exiting program.")
                    break

                


        except Exception as e:
            value = await streamer.get_client().disconnect()
            if value:
                print("Disconnected successfully")
                print(e)

def keyboard_listen():
    while True:
            if keyboard.read_key() == "s":
                global End
                End = True
                break
    

if __name__ == "__main__":  

    while True:

        filename = input("Enter a filename/path to save the logged data to\r\n>>> ")
        if filename.split(".")[-1] != "csv":
            print("Please enter a valid filename with a.csv extension")
            continue
        else:
            break

    keyboard_listen_th = Thread(target=keyboard_listen, daemon=True)
    keyboard_listen_th.start()

    # global End
    while True: 
        try:
            asyncio.run(main())
        except ValueError:
            
            print("Couldn't find WMORE. Attempting to reconnect..")

        if End:
            break
