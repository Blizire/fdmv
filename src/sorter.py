# helps gives a single value to determine if
# a date is larger for the sorter to parse it
def cmp_date(today, expected):
    if( today == expected):
        return 0

    today = today.split("/")
    expected = expected.split("/")
    days = (int(expected[0])  - int(today[0])) * 365
    days += (int(expected[1]) - int(today[1])) * 31
    days += int(expected[2])  - int(today[2])
    return days

def sort_data(data):
    # reorganize the dates to be year/month/day for easier date sorting
    for i in data:
        date = i["date"]
        date = date.split("/")
        date = [date[2], date[0], date[1]]
        date = "/".join(date)
        i["date"] = date

    # remove duplicates
    data = [dict(t) for t in {tuple(d.items()) for d in data}]

    # sort by date and distance
    return sorted(data, key=lambda k: (cmp_date("2022/8/31",k['date']), int(k["dist"])))
