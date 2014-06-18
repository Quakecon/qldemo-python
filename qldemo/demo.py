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

# Constants and enum maps
from qldemo.constants import *

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
        self.string = ' '.join(string.split()[1:])

 
class QLDemo:
    def __init__(self, filename):
        self.gamestate = Gamestate()
        self.players = []
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
        elif string.startswith('n\\'):
            fields = string.split('\\')
            player = {}
            for x in range(0, len(fields), 2):
                player[fields[x]]=fields[x+1]
            self.players.append(player)
        else:
            self.gamestate.config[str(i)]=string
        self.gamestate.configstring[i]=string

    def parse_baseline(self):
        return {'type': 'baseline'}

    def parse_servercommand(self):
        seq = huffman.readlong()
        string = huffman.readstring()
        
        cmd = string.split()[0]
        string = ' '.join(string.split()[1:])
        return {'type': 'servercommand',
                'seq': seq,
                'cmd': cmd,
                'string': string}

    def parse_playerstate(self):
        return {'type': 'playerstate'}



