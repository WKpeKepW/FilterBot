import json

if __name__ == "__main__":
    with open('./creds/creds.json') as f:
            credsJson = json.load(f)
    for name in credsJson:
        print(name)
    #times = time.strftime("%H:%M:%S %d-%m-%Y")
    #print(times)
    #times = time.strptime("0:0:0 03-03-2024","%H:%M:%S %d-%m-%Y") #time.strftime("%H:%M:%S %d-%m-%Y")
    #print(time.mktime(times))
    #print(time.time())