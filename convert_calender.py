#!/usr/bin/env python3
import argparse
import re

MUCAL_ORIGIN = 2459553


def is_leap_year(mu_year):
    return (mu_year % 4 == 0 and mu_year % 100 != 100) or mu_year % 400 == 0


def is_leap_month(mu_month, is_leap_year):
    """
    leap 11 31
     0   0   1
     0   1   0
     1   0   1
     1   1   1

    leap or not 11
    """
    return mu_month % 2 == 1 and (is_leap_year or mu_month != 11)


def length_of_year(mu_year):
    return 366 if is_leap_year(mu_year) else 365


def length_of_month(mu_month, is_leap_year):
    return 31 if is_leap_month(mu_month, is_leap_year) else 30


def day_in_year_to_month_and_day(day_in_year: int, is_leap_year: bool) -> tuple[int, int]:
    mu_month = 0
    mu_day = 0
    while True:
        if day_in_year >= length_of_month(mu_month, is_leap_year):
            day_in_year -= length_of_month(mu_month, is_leap_year)
            mu_month += 1
        else:
            mu_day = day_in_year
            break
    return (mu_month, mu_day)


def month_and_day_to_day_in_year(mu_month: int, mu_day: int, is_leap_year: bool) -> int:
    result = 0
    for m in range(mu_month):
        result += length_of_month(m, is_leap_year)
    result += mu_day
    return result


def JDN_to_mucal(JDN: int) -> tuple[int, int, int]:
    raw_muday = JDN - MUCAL_ORIGIN
    mu_year = 0
    mu_month = 0
    mu_day = 0

    if raw_muday > 0:
        while True:
            if raw_muday >= length_of_year(mu_year):
                raw_muday -= length_of_year(mu_year)
                mu_year += 1
            else:
                mu_month, mu_day = day_in_year_to_month_and_day(raw_muday, is_leap_year(mu_year))
                break
    elif raw_muday < 0:
        while True:
            if raw_muday < 0:
                raw_muday += length_of_year(mu_year - 1)
                mu_year -= 1
            else:
                mu_month, mu_day = day_in_year_to_month_and_day(raw_muday, is_leap_year(mu_year))
                break
    return (mu_year, mu_month, mu_day)


def mucal_to_JDN(mu_year: int, mu_month: int, mu_day: int) -> int:
    JDN = MUCAL_ORIGIN
    if mu_year >= 0:
        for y in range(mu_year):
            JDN += length_of_year(y)
        JDN += month_and_day_to_day_in_year(mu_month, mu_day, is_leap_year(mu_year))
    else:
        for y in range(mu_year + 1, 0):
            JDN -= length_of_year(y)
        JDN -= length_of_year(mu_year) - month_and_day_to_day_in_year(mu_month, mu_day, is_leap_year(mu_year))
    return JDN


def main():
    parser = argparse.ArgumentParser(prog="convert_calender.py", description="convert JDN to and from mulan calender")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-j", "--julian", type=int)
    group.add_argument("-m", "--mucal", type=str)
    args = parser.parse_args()
    if args.julian is not None:
        mu_year, mu_month, mu_day = JDN_to_mucal(args.julian)
        print(f"y{mu_year}-m{mu_month}-d{mu_day}")
    else:
        match = re.match(r"y(?P<mu_year>-?\d+)-m(?P<mu_month>\d+)-d(?P<mu_day>\d+)", args.mucal)
        JDN = mucal_to_JDN(int(match.group("mu_year")), int(match.group("mu_month")), int(match.group("mu_day")))
        print(JDN)


if __name__ == "__main__":
    main()
