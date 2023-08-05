import dateparser

for date_str in dateparser.find_dates('vr 18 feb. 2022', source=True):
    print(date_str)

