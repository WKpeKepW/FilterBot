from mpsiemlib.common import Settings, Creds, MPSIEMAuth 
from mpsiemlib.modules import Filters, EventsAPI
import json
import time
import traceback

class Filter:
    def __init__(self, namePlatform):
        print("constructor")
        creds = Creds()
        creds.core_auth_type = 0
        listCred = self.__CredsPlatformIndex(namePlatform)
        creds.core_hostname = listCred["hostname"]
        creds.core_login = listCred["login"]
        creds.core_pass = listCred["pass"]
        self.auth = MPSIEMAuth(creds,Settings())
        #self.timeStruct = "%H:%M:%S %d-%m-%Y"

    def Query(self, filter, timeFrom, groupBy = [], aggrField = "*", aggrFunc = "COUNT", period = "1d", timeTo = None):
        query = EventsAPI(self.auth,Settings())
        UtimeTo = self.__TimeUnix(timeTo)
        UtimeFrom = self.__TimeUnix(timeFrom)
        try:
            Return = query.get_aggregation_events_by_filter(filter=filter,
                                                    #aggregateBy = [{"function": "COUNT", "field": "*", "unique": False}],
                                                    aggregate_fields=aggrField,
                                                    aggregate_function=aggrFunc,
                                                    groupBy=groupBy,
                                                    time_from=UtimeFrom,
                                                    time_to=UtimeTo,
                                                    period=period
                                                    )
        except Exception as err:
            Return = err #traceback.format_exc()
        query.close()
        return Return
    
    def QueryDowngrade(self, filter, timeFrom, timeTo = None):
        query = EventsAPI(self.auth,Settings())
        UtimeTo = self.__TimeUnix(timeTo)
        UtimeFrom = self.__TimeUnix(timeFrom)
        try:
            self.Return = query.get_count_events_by_filter(filter=filter,
                                                    time_from=UtimeFrom,
                                                    time_to=UtimeTo,
                                                    )
        except Exception as err:
            self.Return = err #traceback.format_exc()
        query.close()


    def FilterPDQLExemple(self, nameFilter):
        filters = Filters(self.auth,Settings())
        All_filter_list = filters.get_filters_list()
        for uuid in All_filter_list:
            #buff = All_filter_list[uuid]["name"]
            if All_filter_list[uuid]["name"] == nameFilter:
                Return = filters.get_filter_info(uuid)
                filters.close()
                return Return
        filters.close()
        return None

    def __TimeUnix(self, Time):
        if str(Time).isdigit():
            return Time
        elif Time:
            return time.mktime(time.strptime(Time, "%H:%M:%S %d-%m-%Y"))
        else:
            return time.time()
        
    def __CredsPlatformIndex(self, name):
        with open('./creds/creds.json') as f:
            credsJson = json.load(f)
        i = 0
        while i < len(credsJson):
            if name == credsJson[i]["name"]:
                return credsJson[i]
            i += 1