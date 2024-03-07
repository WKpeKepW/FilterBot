from filter import Filter
import json
import re
import threading
    #filter.Test()#print(filter.FilterPDQLExemple("Срабатывание правил корреляции"))

class Programm():
    def __init__(self, credsPath = None) -> None:
        self.credsJson = self.ConfJson(credsPath)
        #list = self.CheckAll(filter="correlation_name != null",timeFrom="0:0:0 03-03-2024")
        #print(self.CheckOne(name = "Tomsk",filter="correlation_names != null",timeFrom="0:0:0 03-03-2024"))
        #print(list)

    def CheckOne(self, name, filter, timeFrom, timeTo = None):
        try:
            f = Filter(name, self.credsJson)
        except:
            return None
        return self.parseResponse(name, f.Query(filter=filter,timeFrom=timeFrom, timeTo=timeTo,period=[])) #17:17:27 03-03-2024
        #print(self.parseResponse(name, response))

    def parseResponse(self, name, response):
        Return = ''
        #print(re.search(r"failed", str(response)))
        if re.search(r"Error", str(response)):
            p = re.search(r"\d..", str(response))
            Return = f'Error ({p.group(0)})'
            return f"{name}: {Return}"
        elif isinstance(response, TypeError):
            return f"{name}: Некорректный тип данных в параметре запроса"
        elif str(response).isdigit():
            return f"{name}: {response}"
        else:
            try:
                for group in response: #default
                    for object in response[group]:
                        Return += f'{str(response[group][object]).strip(".0")}, '
                return f"{name}: {Return[:-2]}"
            except Exception as ass:
                return f"{name}: {ass}"

    def CheckAll(self, filter, timeFrom, timeTo = None):
        thr = list()
        filters = list()
        List = list()
        i = 0
        while i < len(self.credsJson):
            name = self.credsJson[i]["name"]
            try:
                filters.append(Filter(name, self.credsJson))
            except Exception as ass:
                List.append(f"{name}: Error 400 Authentification")
                i += 1
                continue
            thr.append(threading.Thread(target=filters[len(filters)-1].QueryDowngrade, args=(filter, timeFrom, timeTo,)))
            thr[len(thr)-1].start()
            i += 1
        k = 0
        while k < len(thr):
            thr[k].join()
            List.append(self.parseResponse(filters[k].name, filters[k].Return))
            k += 1
        return List

    def ConfJson(self, credsPath):
        if credsPath == None:
            pass #Типа кейринг
             
        with open(credsPath) as f:
            return json.load(f)


if __name__ == "__main__":
    p = Programm(credsPath='./creds/creds.json')
    print(p.CheckAll(filter="correlation_name != null",timeFrom="0:0:0 05-03-2024"))