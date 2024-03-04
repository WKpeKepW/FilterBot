from filter import Filter

if __name__ == "__main__":
    filter = Filter("Sib")
    print(filter.Query(filter="correlation_name != null",timeFrom="11:41::53")) #17:17:27 03-03-2024
    #filter.Test()#print(filter.FilterPDQLExemple("Срабатывание правил корреляции"))