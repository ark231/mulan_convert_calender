#!/usr/bin/env python3
import argparse
import re

MUCAL_ORIGIN = 2459553


def is_leap_year(mu_year):
    return (mu_year % 4 == 0 and mu_year % 100 != 100) or mu_year % 400 == 0


def JDN_to_mucal(JDN: int) -> dict[str, int]:
    raw_muday = JDN - MUCAL_ORIGIN
    mu_year = 0
    mu_month = 0
    mu_day = 0

    if raw_muday > 0:
        while True:
            if is_leap_year(mu_year + 1):
                if raw_muday >= 366:
                    raw_muday -= 366
                    mu_year += 1
                else:
                    if (mu_month + 1) % 2 == 0 and raw_muday >= 30:
                        raw_muday -= 30
                        mu_month += 1
                    elif (mu_month + 1) % 2 == 1 and raw_muday >= 31:
                        raw_muday -= 31
                        mu_month += 1
                    else:
                        mu_month = raw_muday
                        break
            else:
                if raw_muday >= 365:
                    raw_muday -= 365
                    mu_year += 1
                else:
                    if ((mu_month + 1) % 2 == 0 or mu_month + 1 == 11) and raw_muday >= 30:
                        raw_muday -= 30
                        mu_month += 1
                    elif ((mu_month + 1) % 2 == 1 and mu_month + 1 != 11) and raw_muday >= 31:
                        raw_muday -= 31
                        mu_month += 1
                    else:
                        mu_day = raw_muday
                        break
    elif raw_muday < 0:
        raise NotImplementedError("negative raw_muday is currently not supported")
    return {"year": mu_year, "month": mu_month, "day": mu_day}


def mucal_to_JDN(mu_year: int, mu_month: int, mu_day: int) -> int:
    JDN = MUCAL_ORIGIN
    if mu_year >= 0:
        for y in range(mu_year):
            if is_leap_year(y):
                JDN += 366 * mu_year
            else:
                JDN += 365 * mu_year
        """
        leap 11 31
         0   0   1
         0   1   0
         1   0   1
         1   1   1

        leap or not 11
        """
        for m in range(mu_month):
            if m % 2 == 1 and (is_leap_year(mu_year) or m != 11):
                JDN += 31
            else:
                JDN += 30
        JDN += mu_day
    else:
        raise NotImplementedError("negative year is currently not supported")
    return JDN


def main():
    parser = argparse.ArgumentParser(prog="convert_calender.py", description="convert JDN to and from mulan calender")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-j", "--julian", type=int)
    group.add_argument("-m", "--mucal", type=str)
    args = parser.parse_args()
    if args.julian is not None:
        mucal = JDN_to_mucal(args.julian)
        print(f"y{mucal['year']}-m{mucal['month']}-d{mucal['day']}")
    else:
        match = re.match(r"y(?P<mu_year>\d+)-m(?P<mu_month>\d+)-d(?P<mu_day>\d+)", args.mucal)
        JDN = mucal_to_JDN(int(match.group("mu_year")), int(match.group("mu_month")), int(match.group("mu_day")))
        print(JDN)


if __name__ == "__main__":
    main()
