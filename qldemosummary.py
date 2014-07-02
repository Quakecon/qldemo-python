#!/bin/env python

## qldemo2json.py
## Shawn Nock, 2014

import argparse
import json
import os
import sys
import time

from qldemo import QLDemo, gametype_to_string
from qldemo.data import GameState, Snapshot
from qldemo.constants import userinfo_map, GT_TEAM, TEAM_STRING_MAP

## Configuration ##

URL_PREFIX='/demos/'
playerinfo_override = {'n': 'name',    ## The userInfo_t summary in
                       'cn': 'clan',   ## CS_PLAYER[MAX_PLAYERS] has short
                       'xcn': 'xclan', ## hard to decipher names. Any map
                       'w': 'wins',    ## here will override the name 
                       'l': 'losses',
                       't': 'team'}

### END Configuration

def main():
    parser = argparse.ArgumentParser(
        description='Summarize, in JSON a QuakeLive Demo File (dm_73)')
    parser.add_argument('file',
                        help='path of the dm_73 file to summarize')
    args = parser.parse_args()

    d = QLDemo(args.file)
    list(d)

    ## Munge playerInfo to conform to ColonelPanic's Needs
    players=[]
    for clientNum, player in d.gamestate.players.items():
        for key, value in player.items():
            new_name=playerinfo_override.get(key, None)
            if new_name:
                player[new_name]=player[key]
                del(player[key])
        # If it's a game where teams make sense, translate the teamId into a team name
        if int(d.gamestate.config['serverinfo']['g_gametype']) >= GT_TEAM:
            player['team']=TEAM_STRING_MAP[player['team']]
        players.append(player)

    # Calculate demo duration
    ## FIXME - I think serverTime is in msec, but it is a guess based
    ## on a skim of the Q3A source. It'd be nice to verify
    first_snap=None
    last_snap=None
    for i in d.packets:
        if i.__class__ is Snapshot:
            first_snap=i
            break
    for i in range(-1,-5,-1):
        if d.packets[i].__class__ is Snapshot:
            last_snap=d.packets[i]
            break
    duration = (last_snap.serverTime - first_snap.serverTime) / 1000
    
    output = {'filename': args.file.split(os.sep)[-1],
              'gametype': gametype_to_string(
                  d.gamestate.config['serverinfo']['g_gametype']),
              'players': d.gamestate.players,
              'size': os.stat(args.file).st_size,
              'pov': d.gamestate.clientNum,
              'timestamp': time.ctime(float(d.gamestate.config['serverinfo']['g_levelStartTime'])),
              'mapname': d.gamestate.config['serverinfo']['mapname'],
              'duration': duration}

    if d.scores:
        output['scores'] = d.scores[-1]
    elif int(d.gamestate.config['serverinfo']['g_gametype']) >= GT_TEAM:
        output['scores']={}
        output['scores']['TEAM_RED'] = {
            'score': d.gamestate.config['scores1'].strip('"')}
        output['scores']['TEAM_BLUE'] = {
            'score': d.gamestate.config['scores2'].strip('"')}

    if int(d.gamestate.config['serverinfo']['g_gametype']) >= GT_TEAM:
        output['teams'] = {}
        output['teams']['TEAM_RED'] = {}
        output['teams']['TEAM_RED']['name'] = d.gamestate.config['redteamname']
        output['teams']['TEAM_RED']['clan'] = d.gamestate.config['redteamclantag']
        output['teams']['TEAM_RED']['timeouts_left'] = d.gamestate.config['timeouts_red']
        output['teams']['TEAM_RED']['score'] = output['scores']['TEAM_RED']
        output['teams']['TEAM_BLUE'] = {}
        output['teams']['TEAM_BLUE']['name'] = d.gamestate.config['blueteamname']
        output['teams']['TEAM_BLUE']['clan'] = d.gamestate.config['blueteamclantag']
        output['teams']['TEAM_BLUE']['timeouts_left'] = d.gamestate.config['timeouts_blue']
        output['teams']['TEAM_BLUE']['score'] = output['scores']['TEAM_BLUE']
        victor = 'TEAM_RED' if int(output['scores']['TEAM_RED']) > int(output['scores']['TEAM_BLUE']) else None
        victor = 'TEAM_BLUE' if int(output['scores']['TEAM_BLUE']) > int(output['scores']['TEAM_RED']) else victor
        output['victor'] = victor
    else: # DUEL, likely doesn't work for FFA
        output['scores'][d.gamestate.config['1stplayer']]['score'] = d.gamestate.config['scores1'].strip('"')
        output['scores'][d.gamestate.config['2ndplayer']]['score'] = d.gamestate.config['scores2'].strip('"')
        victor = d.gamestate.config['1stplayer'] if int(output['scores'][d.gamestate.config['1stplayer']]['score']) > int(output['scores'][d.gamestate.config['2ndplayer']]['score']) else None
        victor = d.gamestate.config['2ndplayer'] if int(output['scores'][d.gamestate.config['2ndplayer']]['score']) > int(output['scores'][d.gamestate.config['1stplayer']]['score']) else victor
        output['victor'] = victor

    json.dump(output, 
              sys.stdout, 
              ensure_ascii=False,
              indent=2,
              sort_keys=True)
    return 0

if __name__ == '__main__':
    main()


