#!/bin/env python

## qldemo2json.py
## Shawn Nock, 2014

import os
import json
import argparse
import sys
from qldemo import QLDemo

parser = argparse.ArgumentParser(description='Summarize, in JSON a QuakeLive Demo File (dm_73)')
parser.add_argument('file',
                   help='path of the dm_73 file to summarize')

args = parser.parse_args()

def main():
    d = QLDemo(args.file)
    json.dump(list(d), sys.stdout, ensure_ascii=False, indent=2)
    return 0

if __name__ == '__main__':
    main()


