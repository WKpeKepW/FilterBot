import time

if __name__ == "__main__":
    times = time.strftime("%H:%M:%S %d-%m-%Y")
    print(times)
    times = time.strptime("0:0:0 03-03-2024","%H:%M:%S %d-%m-%Y") #time.strftime("%H:%M:%S %d-%m-%Y")
    print(time.mktime(times))
    #print(time.time())