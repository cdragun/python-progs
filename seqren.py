#!/usr/bin/env python
#
# seqren.pl
# ---------
# Copyright (c) 2017 Chandranath Gunjal. Available under the MIT License
#
# Rename given files in a sequential order as prefix_nnn
#
# Flags:
#    -d         dry run (don't rename the files yet)
#    -s nnn     starting number (defaults to 1)
#    -p prefix  new filename prefix
#
import getopt
import os.path
import sys

# Main
# ====
if __name__ == '__main__':
    synopsis = 'usage: seqren.py [-d] [-s nnn] -p prefix files...'

    # print usage and exit
    def usage():
        print(synopsis)
        sys.exit(2)


    # parse command line
    def parse_args(argv):
        try:
            opts, args = getopt.getopt(argv, 'hds:p:', ['help'])
        except getopt.GetoptError:
            usage()

        p_dryrun = False
        p_seqno = 1
        p_prefix = None
        for opt, arg in opts:
            if opt in ['-h', '--help']:
                usage()
            elif opt == '-d':
                p_dryrun = True
            elif opt == '-s':
                p_seqno = int(arg)
            elif opt == '-p':
                p_prefix = arg

        if (p_prefix is None) or (len(args) == 0) or (p_seqno < 0):
            usage()

        return p_prefix, p_seqno, p_dryrun, args


    # parse arguments
    prefix, seqno, dryrun, flist = parse_args(sys.argv[1:])

    for x in flist:
        # valid file?
        if not (os.path.exists(x) and os.path.isfile(x)):
            print('{:s} skipped - not a file or doesn\'t exist'.format(x))
            continue

        path, fname = os.path.split(x)
        oldname, extn = os.path.splitext(fname)
        newname = '{:s}_{:03d}{:s}'.format(prefix, seqno, extn)
        y = os.path.join(path, newname)

        # does a file with the new name exist?
        if os.path.exists(y):
            print(
                '{:s} skipped - a file with the new name {:s} already exists'.
                format(x, y))
            continue

        seqno += 1
        print(x, '--->', y)
        if not dryrun:
            os.rename(x, y)
