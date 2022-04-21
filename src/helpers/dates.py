def getPrettySeconds(s: int) -> str:
    """Given an amount of seconds, return a formatted string with
    hours, minutes and seconds; taken from
    https://stackoverflow.com/a/775075/2972183"""
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:d}h:{m:02d}m:{s:02d}s"

def isNowInTimePeriod(startTime, endTime, nowTime): 
    """Compares three times to see if the now Time is inside the period
    https://stackoverflow.com/questions/10048249/how-do-i-determine-if-current-time-is-within-a-specified-range-using-pythons-da"""
    if startTime < endTime: 
        return nowTime >= startTime and nowTime <= endTime 
    else: 
        #Over midnight:
        return nowTime >= startTime or nowTime <= endTime 
