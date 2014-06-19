#!/bin/env python

## qldemo2json.py
## Shawn Nock, 2014

import argparse
import datetime
import json
import re
import os
import sys
import time

from qldemo import QLDemo, gametype_to_string
from qldemo.constants import userinfo_map, GT_TEAM

## Configuration ##

URL_PREFIX='/demos/'
playerinfo_override = {'n': 'name',    ## The userInfo_t summary in
                       'cn': 'clan',   ## CS_PLAYER[MAX_PLAYERS] has short
                       'xcn': 'xclan', ## hard to decipher names. Any map
                       'w': 'wins',    ## here will override the name 
                       'l': 'losses',
                       't': 'team'}

### How should we extract and format a timestamp from the filename
timestamp_re = re.compile('([0-9]{4})_([0-9]{2})_([0-9]{2})-([0-9]{2})_([0-9]{2})_([0-9]{2})')
def timestamp(filename):
    hit = timestamp_re.search(filename)
    if not hit:
        return time.ctime(os.path.getctime(filename))
    return datetime.datetime.strptime(
        hit.group(0), 
        "%Y_%m_%d-%H_%M_%S").ctime()

### How should we extract/format a POV playername from a filename
pov_res = [re.compile('-([a-zA-Z0-9]*)\(POV\)-'),
           re.compile('-([a-zA-Z0-9]*)-'),
           re.compile('\[([a-zA-Z0-9]*)\]-')]
color_tag_re = re.compile('\^[0-9]')
def pov(d, filename):
    for regex in pov_res:
        hit = regex.search(filename)
        if not hit:
            continue
        for i in range(1,regex.groups+1):
            for player in d.gamestate['players']:
                if hit.group(i).find(color_tag_re.sub('', player['name'])) > -1:
                    return player['name']
    return None

### END Configuration

def main():
    parser = argparse.ArgumentParser(
        description='Summarize, in JSON a QuakeLive Demo File (dm_73)')
    parser.add_argument('file',
                        help='path of the dm_73 file to summarize')
    args = parser.parse_args()

    d = QLDemo(args.file)
    gamestate=None
    for packet in d:
        if packet['type'] == 'gamestate':
            gamestate=packet
            break
    if not gamestate:
        return 1

    ## Munge playerInfo to conform to ColonelPanic's Needs
    for player in gamestate['players']:
        for key, value in player.iteritems():
            new_name=dict(userinfo_map.items()+playerinfo_override.items()).get(key, None)
            if new_name:
                player[new_name]=player[key]
                del(player[key])
        player['score']=""
        # If it's a game where teams make sense, translate the teamId into a team name
        if int(gamestate['config']['server_info']['g_gametype']) >= GT_TEAM:
            player['team']=[team['name'] for team in d.gamestate['teams'] if team['id']==int(player['team'])][0]
    
    output = {'filename': args.file,
              'url': ''.join([URL_PREFIX, args.file.split(os.sep)[-1]]),
              'gametype': gametype_to_string(
                  gamestate['config']['server_info']['g_gametype']),
              'players': gamestate['players'],
              'size': os.stat(args.file).st_size,
              'by': pov(d, args.file),
              'timestamp': timestamp(args.file),
              'duration': None,
              'victor': None}
    
    ## Add team list, if it's a team type of game
    if int(gamestate['config']['server_info']['g_gametype']) >= GT_TEAM:
        output['teams']=d.gamestate['teams']
        for team in output['teams']:
            team['score']=""
    
    json.dump(output, 
              sys.stdout, 
              ensure_ascii=False,
              indent=2)
    return 0

if __name__ == '__main__':
    main()


