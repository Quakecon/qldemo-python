#!/bin/env python

## ql-demo-parse.py
## Shawn Nock, 2014

# Standard Lib
import copy
import json
import os
import re
import struct

# C-Extension wrapping Q3A Huffman Routines
import huffman
import struct

# Constants and enum maps
from qldemo.constants import *
from qldemo.data import (GameState, EntityState, PlayerState, 
                         EntityStateNETF, PlayerStateNETF,
                         ServerCommand)

# Configuration

# Utility Functions

# Classes
 
class QLDemo:
    gamestate=GameState()
    packets=[]

    def __init__(self, filename):
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
            self.packets.append(r)
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
        self.gamestate.clientNum = huffman.readlong()
        self.gamestate.checksumFeed = huffman.readlong()
        return self.gamestate

    def parse_configstring(self):
        i = huffman.readshort()
        string = huffman.readbigstring()
        dest=self.gamestate.configstrings
        fieldname=str(i)
        output=string
        if CS_STRING_MAP.get(i, None):
            dest=self.gamestate.config
            fieldname=CS_STRING_MAP.get(i)
        if string.startswith("\\"):
            output={}
            subfields = string.split('\\')
            if not fieldname in dest:
                dest[fieldname]={}
            for x in range(1, len(subfields)-1, 2):
                output[subfields[x]]=subfields[x+1]
        if i >= CS_PLAYERS and i < CS_PLAYERS+MAX_CLIENTS:
            clientNum = i-CS_PLAYERS
            dest=self.gamestate.config
            fieldname='player{:02d}'.format(clientNum)
            subfields = string.split('\\')
            output = {}
            for x in range(0, len(subfields), 2):
                output[subfields[x]]=subfields[x+1]
            if output['t'] == TEAM_SPECTATOR:
                self.gamestate.spectators[clientNum]=output
            else:
                self.gamestate.players[clientNum]=output
        if i >= CS_SOUNDS and i < CS_SOUNDS+MAX_SOUNDS:
            dest=self.gamestate.config
            fieldname='sound'+str(i-CS_SOUNDS)
        if i >= CS_LOCATIONS and i < CS_LOCATIONS+MAX_LOCATIONS:
            dest=self.gamestate.config
            fieldname='location'+str(i-CS_LOCATIONS)
        dest[fieldname]=output

    def parse_baseline(self):
        newnum = huffman.readbits(GENTITYNUM_BITS)
        null_state=EntityState()
        baseline = self.read_delta_entity(null_state, newnum)
        self.gamestate.baselines[newnum]=baseline

    def read_delta_entity(self, frm, num):
        ## Check for server order to remove a baseline
        if huffman.readbits(1):
            # Don't know how we should handle this, it does mean no
            # new data; skipping for now
            return
        ## Check for 'no delta' flag
        if not huffman.readbits(1):
            ## No changes, we should make 'from' a copy of
            ## 'to'... skipping for now
            return

        last_field = huffman.readbyte()
        entity = EntityState()
        netf = EntityStateNETF(entity)

        for i in range(0, last_field):
            if huffman.readbits(1) :
                if not netf.bits[i] :
                    if huffman.readbits(1):
                        if not huffman.readbits(1):
                            netf.fields[i] = huffman.readbits(FLOAT_INT_BITS)
                        else :
                            netf.fields[i] = huffman.readfloat()
                else:
                    if huffman.readbits(1):
                        bits = netf.bits[i]
                        netf.fields[i] = huffman.readbits(bits)

        netf.update()
        return entity

    def parse_servercommand(self):
        seq = huffman.readlong()
        string = huffman.readstring()
        
        return ServerCommand(seq, string)

    def parse_playerstate(self):
        pass



