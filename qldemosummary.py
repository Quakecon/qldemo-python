#!/bin/env python

## qldemo2json.py
## Shawn Nock, 2014

import os
import json
import argparse
import sys
import datetime
from qldemo import QLDemo, gametype_to_string
from qldemo.constants import userinfo_map

playerinfo_override = {'n': 'name',
                       'cn': 'clan',
                       'xcn': 'xclan',
                       'w': 'wins',
                       'l': 'losses',
                       't': 'team'}

def main():
    parser = argparse.ArgumentParser(
        description='Summarize, in JSON a QuakeLive Demo File (dm_73)')
    parser.add_argument('file',
                        help='path of the dm_73 file to summarize')
    args = parser.parse_args()

    d = QLDemo(args.file)
    list(d) # Initiate parse of all packets
    
    output = {}
    output['filename'] = args.file
    output['gametype'] = gametype_to_string(
        d.gamestate['config']['server_info']['g_gametype'])
    for player in d.gamestate['players']:
        for key, value in player.iteritems():
            new_name=dict(userinfo_map.items()+playerinfo_override.items()).get(key, None)
            if new_name:
                player[new_name]=player[key]
                del(player[key])
        player['score']=""
        player['team']=[team['name'] for team in d.gamestate['teams'] if team['id']==int(player['team'])][0]
    output['players']=d.gamestate['players']
    output['num_players']=len(d.gamestate['players'])
    output['size']=os.stat(args.file).st_size
    output['teams']=d.gamestate['teams']
    for team in output['teams']:
        team['score']=""
    output['by']=""
    filename_fields = args.file.split('-')
    ts_string='-'.join(filename_fields[-2:])[:-6]
    #dt=datetime.datetime(0,0,0)
    dt = datetime.datetime.strptime(ts_string, "%Y_%m_%d-%H_%M_%S")
    output['timestamp']=dt.ctime()
    output['duration']=""
    output['victor']=""
    
    json.dump(output, 
              sys.stdout, 
              ensure_ascii=False,
              indent=2)
    return 0

if __name__ == '__main__':
    main()


