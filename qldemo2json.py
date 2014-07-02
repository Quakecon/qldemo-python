#!/bin/env python

## qldemo2json.py
## Shawn Nock, 2014

DEMO_PATH='demos/'
OUTPUT_PATH='api/'

import argparse
import os
import json
import sys

from qldemo import QLDemo

def main():
    parser = argparse.ArgumentParser(
        description='Summarize, in JSON a QuakeLive Demo File (dm_73)')
    parser.add_argument('file',
                        help='path of the dm_73 file to summarize')
    args = parser.parse_args()

    d = QLDemo(args.file)
    list(d)
    json.dump([packet.flatten() for packet in d.packets], 
              sys.stdout, sort_keys=True, ensure_ascii=False, indent=2)
    #json.dump(d.scores, sys.stdout, sort_keys=True, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()


