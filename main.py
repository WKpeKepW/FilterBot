from filter import Filter
import json
import re
import threading
    #filter.Test()#print(filter.FilterPDQLExemple("Срабатывание правил корреляции"))

class Programm():
    def __init__(self) -> None:
        list = self.CheckAll(filter="correlation_name != null",timeFrom="0:0:0 03-03-2024")
        #print(self.CheckOne(name = "Tomsk",filter="correlation_names != null",timeFrom="0:0:0 03-03-2024"))
        print(list)

    def CheckOne(self, name, filter, timeFrom, timeTo = None):
        f = Filter(name)
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
            for group in response: #default
                for object in response[group]:
                    Return += f'{str(response[group][object]).strip(".0")}, '
            return f"{name}: {Return[:-2]}"

    def CheckAll(self, filter, timeFrom, timeTo = None):
        with open('./creds/creds.json') as f:
            credsJson = json.load(f)
        thr = list()
        filters = list()
        i = 0
        while i < len(credsJson):
            name = credsJson[i]["name"]
            filters.append(Filter(name))
            thr.append(threading.Thread(target=filters[i].QueryDowngrade, args=(filter, timeFrom,)))
            thr[i].start()
            i += 1
        List = list()
        k = 0
        while k < i:
            thr[k].join()
            List.append(self.parseResponse(name, filters[k].Return))
            k += 1
        return List


if __name__ == "__main__":
    Programm()