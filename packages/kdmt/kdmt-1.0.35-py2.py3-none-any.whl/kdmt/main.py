import dateparser

for date_str in dateparser.find_dates('mar. 1 mars 2022 à 14:04, 4218 Bo2 pirotte.cyndia@gmail.com&gt', source=True):
    print(date_str)

