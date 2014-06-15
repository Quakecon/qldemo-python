#!/bin/env python

## ql-demo-parse.py
## Shawn Nock, 2014

import struct
import huffman

# Constants

## Message Types
SVC_BAD=0
SVC_NOP=1
SVC_GAMESTATE=2
SVC_CONFIGSTRING=3
SVC_BASELINE=4
SVC_SERVERCOMMAND=5
SVC_DOWNLOAD=6
SVC_SNAPSHOT=7
SVC_EOF=8

# Classes
 
class Demo:
    def __init__(self, filename):
        huffman.init()
        huffman.open(filename)

    def __iter__(self):
        while True:
            seq=huffman.readrawlong()
            length=huffman.readrawlong()
            #print("seq {}".format(seq))
            #print("len {}".format(length))
            if seq == -1 or length == -1:
                print("End of File Reached")
                break
            huffman.fill(length)
            ack = huffman.readlong()
            cmd = huffman.readbyte()
            if cmd == SVC_GAMESTATE: 
                self.parse_gamestate()
            elif cmd == SVC_SERVERCOMMAND: 
                self.parse_servercommand()
            elif cmd == SVC_SNAPSHOT: 
                self.parse_playerstate()
            yield cmd

    def parse_gamestate(self):
        print("Gamestate")
        print(huffman.readlong())
        while True:
            cmd = huffman.readbyte()
            if cmd == SVC_EOF:
                break
            elif cmd == SVC_CONFIGSTRING: 
                self.parse_configstring()
            elif cmd == SVC_BASELINE: 
                self.parse_baseline()

    def parse_configstring(self):
        i = huffman.readshort()
        string = huffman.readbigstring()
        print(i, string.replace('\\',"\n"))

    def parse_baseline(self):
        pass

    def parse_servercommand(self):
        print("Server Command")
        pass

    def parse_playerstate(self):
        print("Player State")
        pass

def main():
    d = Demo('test.dm_73')
    for packet in d:
        pass

if __name__ == '__main__':
    main()


