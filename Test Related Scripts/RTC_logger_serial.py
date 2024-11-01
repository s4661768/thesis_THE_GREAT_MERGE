import serial, time 

# from serial.tools import list_ports
import keyboard
from threading import Thread
import os
import pandas as pd

RTC = 0
SYS_TIME = 1

global End 
End = False
global filename
filename = "./temp.csv"

# ports = serial.tools.list_ports.comports()


while True:

    filename = input("Enter a filename/path to save the logged data to\r\n>>> ")
    if filename.split(".")[-1] != "csv":
        print("Please enter a valid filename with a.csv extension")
        continue
    else:
        break

# for port, desc, _ in sorted(ports):
#     print(f"{port}: {desc}")

# input = input("Enter the COMPORT number and baud rate for the desired connect. E.G for COM7 at 115200 enter:\r\n7 115200\r\n>>> ")
# num = int(input.split(" ")[0])
# baud = int(input.split(" ")[1])
# print(f"Attempting to connect to COM{num} at {baud} Baud\r\n")


# print("COM" + input.split(" ")[0])

ser = serial.Serial()
# ser.baudrate = baud
# ser.port = "COM" + input.split(" ")[0]
ser.baudrate = 115200
ser.port = "COM12"
ser.open()

temp_file = "./temp.csv"

def del_temp():
    if os.path.exists('C:\\Users\\prism\\OneDrive\\Documents\\2024\\Uni\\Thesis\\Test Related Scipts\\temp.csv'):
        os.remove("C:\\Users\\prism\\OneDrive\\Documents\\2024\\Uni\\Thesis\\Test Related Scipts\\temp.csv")

def listen():
    global End
    
    data = []

    while True:
        l = ser.readline()
        if len(l) < 80:
            
            continue

        # print(l)
        try:
            rtc_line = (str(l).split(","))[1]
            sys_time = time.time()
            data.append([rtc_line, sys_time])
        except IndexError:
            print("Invalid data format. Skipping this line.")
            continue        
        
        print(rtc_line)
        
        
        
        if End:
            
            ser.close()
            print("Stopped listening...")
            print("Writing to file now...")
            print(data)
            # with open(temp_file, "a") as f:
            #     for line in data:
            #         f.writelines(str(line) + "\r\n")
                    
                
            # f.close()
            global filename
            df = pd.DataFrame(data, columns=['RTC_TIME', 'SYS_TIME'])
            df.to_csv(filename, index=False)
            print("Writing complete... Exiting program.")
            break

def main(): 
    del_temp()
    listen_th = Thread(target=listen)
    listen_th.setDaemon(True)
    listen_th.start()
    while True:
        if keyboard.read_key() == "s":
            global End
            End = True
            listen_th.join()
            break

if __name__ == "__main__":
    main()