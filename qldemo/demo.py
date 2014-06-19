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

# Constants and enum maps
from qldemo.constants import *

# Configuration

# Classes

class ServerCommand:
    seq = None
    cmd = None
    string = None

    def __init__(self, seq, string):
        self.seq = seq
        self.cmd = string.split()[0]
        self.string = ' '.join(string.split()[1:])

class PlayerState:
    def __init__(self):
        pass

class EntityState:
    pass

 
class QLDemo:
    gamestate={
        'type': 'gamestate',
        'configstrings': {},
        'config': {},
        'players': [],
        'spectators': [],
        'teams': [],
        'baselines': [],
    }

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
                continue
                self.parse_baseline()
        self.gamestate['clientNum'] = huffman.readlong()
        self.gamestate['checksumFeed'] = huffman.readlong()
        return self.gamestate

    def parse_configstring(self): 
        i = huffman.readshort()
        string = huffman.readbigstring()
        dest=self.gamestate['configstrings']
        fieldname=str(i)
        output=string
        if CS_STRING_MAP.get(i, None):
            dest=self.gamestate['config']
            fieldname=CS_STRING_MAP.get(i)
        if string.startswith("\\"):
            output={}
            subfields = string.split('\\')
            if not fieldname in dest:
                dest[fieldname]={}
            for x in range(1, len(subfields)-1, 2):
                output[subfields[x]]=subfields[x+1]
        if i >= CS_PLAYERS and i < CS_PLAYERS+MAX_CLIENTS:
            dest=self.gamestate['config']
            fieldname='player{:02d}'.format(i-CS_PLAYERS)
            subfields = string.split('\\')
            output = {}
            for x in range(0, len(subfields), 2):
                output[subfields[x]]=subfields[x+1]
            output['id']=i-CS_PLAYERS
            if output['t'] == TEAM_SPECTATOR:
                self.gamestate['spectators'].append(output)
            else:
                self.gamestate['players'].append(output)
        if i >= CS_SOUNDS and i < CS_SOUNDS+MAX_SOUNDS:
            dest=self.gamestate['config']
            fieldname='sound'+str(i-CS_SOUNDS)
        if i >= CS_LOCATIONS and i < CS_LOCATIONS+MAX_LOCATIONS:
            dest=self.gamestate['config']
            fieldname='location'+str(i-CS_LOCATIONS)
        if 'system_info' in self.gamestate['config'] \
           and self.gamestate['config']['system_info'].get('g_gametype', None) \
           and self.gamestate['config']['system_info']['g_gametype'] >= GT_TEAM \
           and i >= CS_TEAM and i < CS_TEAM+MAX_TEAMS:
            dest=self.gamestate['config']
            fieldname='team'+str(i-CS_TEAM+1)
            self.gamestate['teams'].append({'id': i-CS_TEAM+1,
                                            'name': string})
        dest[fieldname]=output

    def parse_baseline(self):
        newnum = huffman.readbits(GENTITYNUM_BITS)
        baseline = EntityState()
        null_state = EntityState()
        self.gamestate['baselines'].append(baseline)
        r = self.read_delta_entity(null_state, baseline, newnum)
        if r is False:
            # Make a copy, there are no changes
            old=self.gamestate['baselines'].pop()
            new=copy.copy(old)
            new.number=newnum
            self.gamestate['baselines'].append(old)
            self.gamestate['baselines'].append(new)

    def read_delta_entity(self, frm, to, num):
        ## Check for server order to remove a baseline
        if huffman.readbits(1):
            # Don't know how we should handle this, it does mean no
            # new data; skipping for now
            return None
        ## Check for 'no delta' flag
        if not huffman.readbits(1):
            ## No changes, we should make 'from' a copy of
            ## 'to'... this is easier to do from the calling
            ## method. Signaling up the chain
            return False

    def parse_servercommand(self):
        seq = huffman.readlong()
        string = huffman.readstring()
        
        cmd = string.split()[0]
        string = ' '.join(string.split()[1:])
        if cmd == 'chat':
            player_to=[ x['n'] for x in
                        self.gamestate['players']+self.gamestate['spectators']
                        if x['id']==int(string[2:4])][0]
            player_to=player_to if player_to else 'FIXME'
            return {'type': 'servercommand',
                    'seq': seq,
                    'cmd': cmd,
                    'to': player_to,
                    'string': string}
        return {'type': 'servercommand',
                'seq': seq,
                'cmd': cmd,
                'string': string}

    def parse_playerstate(self):
        return {'type': 'playerstate'}



