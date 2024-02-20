#!/usr/bin/env python
import tocsv
from datetime import timedelta

MAX_LOWEST = 99999999999999999


def find_lowest(window, lowest):
    if not window:
        return lowest
    return min(window, key=lambda x: x[1])[1]


def main(argv=None):
    args = tocsv.parser().parse_args(argv)
    if args.output:
        out = args.output.open('w')
        out.write(f'time,value,next_value\n')
    window24h = []
    lowest = MAX_LOWEST
    for ts, val in tocsv.read_binary_log(args.binary_log, False):
        window24h.append((ts, val))
        while window24h and (ts - window24h[0][0] > timedelta(hours=24)):
            _, val2 = window24h.pop(0)
            if val2 <= lowest:
                lowest = MAX_LOWEST
        if lowest == MAX_LOWEST:
            lowest = find_lowest(window24h, lowest)
        nval = lowest * 1.1
        line = f'{ts},{val},{nval}'
        if args.output:
            out.write(f'{line}\n')
        print(line)
    while window24h:
        ts2, val2 = window24h.pop(0)
        if val2 <= lowest:
            lowest = find_lowest(window24h, lowest)
        nval = lowest * 1.1
        line = f'{ts2},,{nval}'
        if args.output:
            out.write(f'{line}\n')
        print(line)

    if args.output:
        out.close()


if __name__ == '__main__':
    main()
