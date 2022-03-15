def getPrettySeconds(s: int) -> str:
    """Given an amount of seconds, return a formatted string with
    hours, minutes and seconds; taken from
    https://stackoverflow.com/a/775075/2972183"""
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:d}h:{m:02d}m:{s:02d}s"
