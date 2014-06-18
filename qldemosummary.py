#!/bin/env python

## qldemo2json.py
## Shawn Nock, 2014

import os
import json
import argparse
import sys
from qldemo import QLDemo, gametype_to_string

def main():
    parser = argparse.ArgumentParser(description='Summarize, in JSON a QuakeLive Demo File (dm_73)')
    parser.add_argument('file',
                        help='path of the dm_73 file to summarize')
    args = parser.parse_args()

    d = QLDemo(args.file)
    list(d) # Initiate parse of all packets
    output = {}
    output['filename'] = args.file
    output['gametype'] = gametype_to_string(d.gamestate.config['g_gametype'])
    players_tmp=[]
    #output['players_full']=[]
    p_tmp={}
    for player in d.players:
        if player['so'] != "0" or int(player['t']) > 2:
            continue
        #output['players_full'].append(player)
        p_tmp['name'] = player['n']
        p_tmp['clan'] = player['cn']
        p_tmp['xclan'] = player['xcn']
        p_tmp['country'] = player['c']
        p_tmp['wins'] = player['w']
        p_tmp['loses'] = player['l']
        p_tmp['team'] = player['t']
        players_tmp.append(p_tmp)
        p_tmp={}
    output['players']=players_tmp
    output['num_players']=len(players_tmp)

    
    json.dump(output, 
              sys.stdout, 
              ensure_ascii=False,
              indent=2)
    return 0

if __name__ == '__main__':
    main()


