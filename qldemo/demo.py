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
                         ServerCommand, Snapshot)

# Configuration

# Utility Functions

# Classes
 
class QLDemo:
    gamestate=GameState()
    packets=[]
    snapshots=[]
    scores={}

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
                r = self.parse_snapshot()
                self.snapshots.append(r)
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
            fieldname=int(clientNum)
            subfields = string.split('\\')
            output = {}
            for x in range(0, len(subfields), 2):
                output[subfields[x]]=subfields[x+1]
            if output['t'] == TEAM_SPECTATOR:
                dest=self.gamestate.spectators
            else:
                dest=self.gamestate.players
            self.gamestate.scores[clientNum]=0
        if i >= CS_SOUNDS and i < CS_SOUNDS+MAX_SOUNDS:
            dest=self.gamestate.config
            fieldname='sound'+str(i-CS_SOUNDS)
        if i >= CS_LOCATIONS and i < CS_LOCATIONS+MAX_LOCATIONS:
            dest=self.gamestate.config
            fieldname='location{:02d}'.format(i-CS_LOCATIONS)
        dest[fieldname]=output

    def parse_baseline(self):
        newnum = huffman.readbits(GENTITYNUM_BITS)
        null_state=EntityState()
        baseline = self.read_delta_entity(null_state, newnum)
        ## Broken for now, disabling for speed
        #self.gamestate.baselines[newnum]=baseline

    def read_delta_entity(self, frm, num):
        ## Check for server order to remove a baseline
        if huffman.readbits(1) == 1:
            # Don't know how we should handle this, it does mean no
            # new data; skipping for now
            return
        ## Check for 'no delta' flag
        if huffman.readbits(1) == 0:
            ## No changes, we should make 'from' a copy of
            ## 'to'... skipping for now
            return

        last_field = huffman.readbyte()
        entity = EntityState()
        netf = EntityStateNETF(entity)

        for i in range(0, last_field):
            if huffman.readbits(1) :
                if not netf.bits[i] :
                    if huffman.readbits(1) != 0:
                        if huffman.readbits(1) == 0:
                            netf.fields[i] = huffman.readbits(FLOAT_INT_BITS)
                        else :
                            netf.fields[i] = huffman.readfloat()
                else:
                    if huffman.readbits(1) != 0:
                        netf.fields[i] = huffman.readbits(netf.bits[i])

        netf.update()
        return entity

    def parse_servercommand(self):
        seq = huffman.readlong()
        string = huffman.readstring()
        
        sc=ServerCommand(seq, string)
        if sc.cmd.startswith('scores'):
            score_list=sc.string.split()
            num_scores=int(score_list[0])
            score_field_num=len(score_list[1:])/num_scores
            for i in range(num_scores):
                clientNum = int(score_list[1:][i*score_field_num])
                score = int(score_list[1:][i*score_field_num+1])
                self.gamestate.scores[clientNum]=score
            
        return sc

    def parse_snapshot(self):
        new_snap = Snapshot()
        new_snap.serverTime=huffman.readlong()
        delta_num = huffman.readbyte()
        new_snap.snapFlags = huffman.readbyte()
        new_snap.areamaskLen = huffman.readbyte()
        #for i in range(new_snap.areamaskLen+1):
        #    new_snap.areamask.append(huffman.readbyte())
        #ps = self.parse_playerstate()
        #new_snap.playerstate=ps
        return new_snap

    def parse_playerstate(self):
        last_field=huffman.readbyte()
        player=PlayerState()
        netf=PlayerStateNETF(player)

        playerStateFieldsNum  = len( netf.bits )

        if last_field > playerStateFieldsNum :
            return None

        for i in range( 0, last_field) :
            if huffman.readbits( 1 ) :
                if netf.bits[ i ] == 0 :
                    if huffman.readbits( 1 ) == 0 :
                        netf.fields[ i ] = huffman.readbits( FLOAT_INT_BITS ) - FLOAT_INT_BIAS
                    else :
                        netf.fields[ i ] = huffman.readfloat()
                else :
                    bits = netf.bits[ i ]
                    netf.fields[ i ] = huffman.readbits( bits )
        netf.update()

        if huffman.readbits( 1 ) :
            if huffman.readbits( 1 ) :
                c = huffman.readshort()
                for i in range( MAX_STATS ) :
                    if c & ( 1 << i ) :
                        player.stats[ i ] = huffman.readshort()

            if huffman.readbits( 1 ) :
                c = huffman.readshort()
                for i in range( MAX_PERSISTANT ) :
                    if c & ( 1 << i ) :
                        player.persistant[ i ] = huffman.readshort()

            if huffman.readbits( 1 ) :
                c = huffman.readshort()
                for i in range( MAX_WEAPONS ) :
                    if c & ( 1 << i ) :
                        player.ammo[ i ] = huffman.readshort()

            if huffman.readbits( 1 ) :
                c = huffman.readshort()
                for i in range( MAX_POWERUPS ) :
                    if c & ( 1 << i ) :
                        player.powerups[ i ] = huffman.readlong()

        return player

