def day(date_list):
    Year = date_list[-1] % 400
    Years = date_list[-1] - Year
    Months = (Year % 100)
    RemDays = Year - Months
    Months = Months - 1
    OddDays = 0
    Answer = ""

    CheckingDays = Years % 400
    if CheckingDays == 100:
        OddDays = 5
    elif CheckingDays == 200:
        OddDays = 2
    elif CheckingDays == 300:
        OddDays = 1
    elif CheckingDays == 400:
        OddDays = 0

    CenturyYears = RemDays
    if CenturyYears == 100:
        OddDays += 5
    elif CenturyYears == 200:
        OddDays += 3
    elif CenturyYears == 300:
        OddDays += 1
    elif CenturyYears == 400:
        OddDays += 0

    MonthRemainder = Months // 4
    MonthRemDays = Months - MonthRemainder
    FinalMonthDays = MonthRemDays + (MonthRemainder * 2)
    OddDaysInMonths = FinalMonthDays % 7
    OddDays += OddDaysInMonths

    MonthsOddDays = [3, 0, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3]
    Val = 0
    for i in range(date_list[1] - 1):
        Val += MonthsOddDays[i]
    Val += date_list[0]

    EquateDays = Val % 7

    if date_list[-1] % 4 == 0:
        OddDays += EquateDays + 1
    else:
        OddDays += EquateDays

    if OddDays >= 7:
        OddDays = OddDays % 7

    DaysList = ["Sunday", "Monday", "Tuesday",
                "Wednesday", "Thursday", "Friday", "Saturday"]

    for i in range(len(DaysList)):
        if OddDays == i:
            Answer = DaysList[i]
            break
    return Answer
