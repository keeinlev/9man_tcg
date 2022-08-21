from datetime import datetime, timedelta

def nth_weekday_of_month(n, weekday, month, year):
    """
    n is the week #, must be 1-5
    weekday is int where monday = 0, sunday = 6
    month is int from 1 to 12
    year is int
    can raise exception if either n or month exceed bounds or month does not have 5th weekday
    """
    if (n < 1 or n > 5):
        raise Exception("Invalid value for n")
    if (month < 1 or month > 12):
        raise Exception("Invalid value for month")
    d = datetime(year, month, 7)
    offset = weekday - d.weekday()
    first = d + timedelta(days=offset)
    nth = first + timedelta(days=7*(n-1))
    if nth.month != month:
        raise Exception("Month does not have 5th specified weekday")
    return nth
