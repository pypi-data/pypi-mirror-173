import dateparser

for date_str in dateparser.find_dates('donderdag, 06 oktober 2022, 02:15p.m. 02:00', source=True):
    print(date_str)

