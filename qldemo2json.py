#!/bin/env python

## qldemo2json.py
## Shawn Nock, 2014

DEMO_PATH='demos/'
OUTPUT_PATH='api/'

import os
import json

from qldemo import QLDemo

def main():
    for file in os.listdir(DEMO_PATH):
        if not file.endswith('dm_73'):
            continue
        if os.path.isfile(OUTPUT_PATH+''.join([file[:-5],"json"])):
            print("found existing file")
            continue
        print("Processing: {}".format(file))
        d = QLDemo(DEMO_PATH+file)
        with open(OUTPUT_PATH+''.join([file[:-5],"json"]), 'w') as output_file:
            json.dump(list(d), output_file, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()


