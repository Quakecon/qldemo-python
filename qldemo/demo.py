#!/bin/env python

## ql-demo-parse.py
## Shawn Nock, 2014

# Standard Lib
import json
import os
import re
import struct

# C-Extension wrapping Q3A Huffman Routines
import huffman

# Constants
nick_clan_filter = re.compile('\^[0-7]|\u0019')

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

class Gamestate:
    config = {}
    configstring = {}

class PlayerState:
    pass

class ServerCommand:
    seq = None
    cmd = None
    string = None

    def __init__(self, seq, string):
        self.seq = seq
        self.cmd = string.split()[0]
        if self.cmd == 'chat':
            self.string = filter_qstring(' '.join(string.split()[1:])[4:])
        else:
            self.string = ' '.join(string.split()[1:])

 
class QLDemo:
    def __init__(self, filename):
        self.gamestate = Gamestate()
        self.decoded_packets = []
        huffman.init()
        huffman.open(filename)

    def __iter__(self):
        while True:
            seq=huffman.readrawlong()
            length=huffman.readrawlong()
            if seq == -1 or length == -1:
                break
            huffman.fill(length)
            ack = huffman.readlong()
            cmd = huffman.readbyte()
            if cmd == SVC_GAMESTATE: 
                r = self.parse_gamestate()
            elif cmd == SVC_SERVERCOMMAND: 
                r = self.parse_servercommand()
            elif cmd == SVC_SNAPSHOT:
                continue
                r = self.parse_playerstate()
            yield r

    def parse_gamestate(self):
        ack=huffman.readlong()
        while True:
            cmd = huffman.readbyte()
            if cmd == SVC_EOF:
                break
            elif cmd == SVC_CONFIGSTRING: 
                self.parse_configstring()
            elif cmd == SVC_BASELINE: 
                self.parse_baseline()
        return {'type': 'gamestate',
                'config': self.gamestate.config}

    def parse_configstring(self):
        i = huffman.readshort()
        string = huffman.readbigstring()
        if string.startswith('\\'):
            fields = string.split('\\')
            for x in range(1, len(fields)-1, 2):
                self.gamestate.config[fields[x]]=fields[x+1]
        else:
            self.gamestate.config[str(i)]=string
        self.gamestate.configstring[i]=string

    def parse_baseline(self):
        return {'type': 'baseline'}

    def parse_servercommand(self):
        seq = huffman.readlong()
        string = huffman.readstring()
        
        cmd = string.split()[0]
        if cmd == 'chat':
            string = filter_qstring(' '.join(string.split()[1:])[4:])
        else:
            string = ' '.join(string.split()[1:])
        return {'type': 'servercommand',
                'seq': seq,
                'cmd': cmd,
                'string': string}

    def parse_playerstate(self):
        return {'type': 'playerstate'}

def filter_qstring(string):
    ## Takes out formatting characters in chats, playernames, &c
    return nick_clan_filter.sub('', string)


