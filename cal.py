#!/usr/bin/env python
#
# cal.py
# ------
# Copyright (c) 2017 Chandranath Gunjal. Available under the MIT License
#
#  A friendlier cal - converts month names.
#
#  o With no arguments, print calendar for current month & year
#  o With two arguments, assumes month & year are given
#  o With one argument
#    - the argument is assumed to be a month (if valid) for this year.
#    - a "month+/-" format uses the next/prev year.
#    - a lone "+/-" prints the next/prev month's calendar.
#    - a leading zero forces the argument to be a "year".
#
import calendar
import datetime
import getopt
import sys


def month2num(given):
    """Convert a given month name to numeric"""
    months = ['january', 'february', 'march', 'april',
              'may', 'june', 'july', 'august',
              'september', 'october', 'november', 'december'
              ]

    given = given.lower()
    for i, mth in enumerate(months, 1):
        if mth.startswith(given):
            return i
    return 0


def build_cal_args(args):
    """Determine the year/month. Return list [year] or [year, month]"""
    t = datetime.date.today()
    m, y = t.month, t.year

    x = None
    if len(args) == 0:
        # no args - print default calendar
        x = [y, m]

    elif len(args) == 1:
        # cal + ==> next month
        if args[0] == '+':
            x = [y + 1, 1] if (m == 12) else [y, m + 1]

        # cal - ==> prev month
        elif args[0] == '-':
            x = [y - 1, 12] if (m == 1) else [y, m - 1]

        # cal jun+ or cal 12+ ==> given month for next year
        elif args[0].endswith('+'):
            m = month2num(args[0][:-1])
            x = [y + 1, int(args[0][:-1])] if (m == 0) else [y + 1, m]

        # cal jun- or cal 12- ==> given month for prev year
        elif args[0].endswith('-'):
            m = month2num(args[0][:-1])
            x = [y - 1, int(args[0][:-1])] if (m == 0) else [y - 1, m]

        # cal 0nn ==> assume as year 
        elif args[0].startswith('0'):
            x = [int(args[0])]

        # cal numeric ==> assume as month if in 1..12
        elif args[0].isnumeric():
            m = int(args[0])
            x = [y, m] if (1 <= m <= 12) else [m]

        # cal any ==> convert month if possible or let cal handle it
        else:
            m = month2num(args[0])
            x = [int(args[0])] if (m == 0) else [y, m]

    elif len(args) == 2:
        # cal month year
        m = month2num(args[0])
        x = [int(args[1]), int(args[0])] if (m == 0) \
            else [int(args[1]), m]

    return x


def print_cal(ym):
    """Print calendar for [year, month]."""
    tc = calendar.TextCalendar(firstweekday=6)
    tc.pryear(ym[0]) if len(ym) == 1 else tc.prmonth(ym[0], ym[1])


# Main
# ====
if __name__ == '__main__':
    synopsis = """usage: cal.py -h [mth][+|-] | mth year | [0]year
    Month names (shortened or otherwise) can be used.
    """


    def usage():
        """Print usage and exit"""
        print(synopsis)
        sys.exit(2)


    def parse_args(argv):
        """Parse command line arguments"""
        try:
            opts, args = getopt.getopt(argv, 'h', ['help'])
        except getopt.GetoptError:
            usage()

        for opt, arg in opts:
            if opt in ['-h', '--help']:
                usage()

        if len(args) > 2:
            usage()
        return args


    # main
    alist = parse_args(sys.argv[1:])
    try:
        print_cal(build_cal_args(alist))
    except:
        usage()
