from convert_calender import MUCAL_ORIGIN, JDN_to_mucal, mucal_to_JDN


def main():
    for i in range(MUCAL_ORIGIN - 5 * 365 - 10, MUCAL_ORIGIN + 5 * 365 + 10):
        mu_year, mu_month, mu_day = JDN_to_mucal(i)
        assert i == mucal_to_JDN(mu_year, mu_month, mu_day)
        print(f"y{mu_year}-m{mu_month}-d{mu_day}")


if __name__ == "__main__":
    main()
