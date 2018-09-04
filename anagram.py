#!/usr/bin/env python
#
# anagram.py
# ----------
# Copyright (c) 2017 Chandranath Gunjal. Available under the MIT License
#
# usage: anagram.py [-h] [-c char] [-l x..y] jumble
#
import getopt
import sys
from collections import Counter


class Bag(Counter):
    """Extend Counter to include subset like (<=) comparison"""
    def is_subset(self, other):
        for c, count in self.items():
            if other[c] < count:
                return False
        return True

    def __le__(self, other):
        return self.is_subset(other)


class Anagram:
    """Find anagrams of a given jumble."""
    def __init__(self, jumble, compulsory=None, min_len=-1, max_len=-1):
        self.jumble = jumble.lower()
        self.jdist = Bag(self.jumble)
        self.jlen = len(self.jumble)

        self.compulsory = compulsory
        self.min_len = self.jlen if (min_len < 0) else min_len
        self.max_len = self.jlen if (max_len < 0) else max_len

        self.matches = set()

    def find_matches(self, dictionary='/usr/share/dict/words'):
        with open(dictionary, 'rt') as fh:
            for w in fh:
                w = w.strip()

                wlen = len(w)
                if (wlen < self.min_len) or (wlen > self.max_len):
                    continue
                if (self.compulsory is not None) and (
                        self.compulsory not in w):
                    continue

                # compare letter counts
                wdist = Bag(w.lower())
                if ((wlen > self.jlen) and (self.jdist <= wdist)) \
                        or ((wlen < self.jlen) and (wdist <= self.jdist)) \
                        or ((wlen == self.jlen) and (self.jdist == wdist)):
                    self.matches.add(w)

    def print_results(self):
        for w in sorted(self.matches):
            print(w)


# Main
# ====
if __name__ == '__main__':
    synopsis = 'usage: anagram.py [-h] [-c char] [-l m..M] jumble'
    helptxt = synopsis + """
        -c char      compulsory letter
        -h           help
        -l m..M      min..max word lengths (incomplete specs are valid)
    """


    def print_usage():
        """Print usage and exit."""
        print(helptxt)
        sys.exit(2)


    # parse word length
    def parse_range(spec, sep='..', default_low=1, default_high=40):
        """Parse range specified as x..y or a part thereof."""
        parsed = spec.split(sep)

        x = int(parsed[0]) if parsed[0] != '' else default_low
        if len(parsed) == 2:
            y = int(parsed[1]) if parsed[1] != '' else default_high
        else:
            y = x

        return x, y


    # parse command line
    def parse_args(argv):
        try:
            opts, args = getopt.getopt(argv, 'c:hl:', ['help'])
        except getopt.GetoptError:
            print_usage()

        p_compulsory = None
        p_min = -1
        p_max = -1
        for opt, arg in opts:
            if opt in ['-h', '--help']:
                print_usage()
            elif opt == '-c':
                p_compulsory = arg
            elif opt == '-l':
                p_min, p_max = parse_range(arg)

        if len(args) != 1:
            print_usage()
        p_jumble = args[0]

        return p_jumble, p_compulsory, p_min, p_max


    # parse command line
    jumble, compulsory, len_min, len_max = parse_args(sys.argv[1:])

    # solve the anagram & print
    z = Anagram(jumble, compulsory, len_min, len_max)
    z.find_matches()
    z.print_results()
