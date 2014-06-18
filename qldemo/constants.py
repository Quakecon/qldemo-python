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

## Gametypes
GT_FFA=0                         # free for all
GT_TOURNAMENT=1          # one on one tournament
GT_SINGLE_PLAYER=2       # single player ffa
GT_TEAM=3               # team deathmatch
GT_CTF=4                 # capture the flag
GT_1FCTF=5
GT_OBELISK=6
GT_HARVESTER=7

GT_STRING_MAP={GT_FFA: 'FFA',
               GT_TOURNAMENT: '1v1 Tournament',
               GT_SINGLE_PLAYER: 'Single Player FFA',
               GT_TEAM: 'Team DM',
               GT_CTF: 'CTF',
               GT_1FCTF: '1FCTF',
               GT_OBELISK: 'Obelisk',
               GT_HARVESTER: 'Harvester'}

def gametype_to_string(i):
    i=int(i)
    return GT_STRING_MAP.get(i, None)

MAX_MODELS = 242 # Not the same as Q3A
MAX_SOUNDS = 255 # Not the same as Q3A
MAX_CLIENTS = 64 
MAX_LOCATIONS = 64
MAX_TEAMS = 2 # Made up to filter team names from observed QL demos

# Configstring Definitions from Q3A source headers with mods for QL
CS_SERVERINFO = 0
CS_SYSTEMINFO = 1
CS_MUSIC = 2
CS_MESSAGE = 3               # from the map worldspawn's message field
CS_MOTD = 4               # g_motd string for server message of the day
CS_WARMUP = 5               # server time when the match will be restarted
CS_SCORES1 = 6
CS_SCORES2 = 7
CS_GAME_VERSION = 20
CS_LEVEL_START_TIME = 21   # so the timer only shows the current level
CS_INTERMISSION = 22       # when 1, fraglimit/timelimit has been hit and intermission will start in a second or two
CS_FLAGSTATUS = 23         # string indicating flag status in CTF
CS_SHADERSTATE = 24
CS_BOTINFO = 25
CS_ITEMS = 27              # string of 0's and 1's that tell which items are present
CS_MODELS = 32
CS_SOUNDS = (CS_MODELS+MAX_MODELS)
CS_PLAYERS = (CS_SOUNDS+MAX_SOUNDS)
CS_LOCATIONS = (CS_PLAYERS+MAX_CLIENTS)
CS_PARTICLES  = (CS_LOCATIONS+MAX_LOCATIONS)
CS_MAX = (CS_PARTICLES+MAX_LOCATIONS)
CS_TEAM = 659

CS_STRING_MAP = {CS_SERVERINFO: 'server_info',
                 CS_SYSTEMINFO: 'system_info',
                 CS_MUSIC: 'music',
                 CS_MESSAGE: 'map_message',
                 CS_MOTD: 'server_motd',
                 CS_WARMUP: 'match_restart',
                 CS_SCORES1: 'scores1',
                 CS_SCORES2: 'scores2',
                 CS_GAME_VERSION: 'game_version',
                 CS_LEVEL_START_TIME: 'level_start_time',
                 CS_INTERMISSION: 'intermission',
                 CS_FLAGSTATUS: 'ctf_flag_status',
                 CS_SHADERSTATE: 'shader_state',
                 CS_BOTINFO: 'bot_info',
                 CS_ITEMS: 'items_present',
                 CS_MODELS: 'models',
                 CS_SOUNDS: 'sounds',
                 CS_PLAYERS: 'players',
                 CS_LOCATIONS: 'locations',
                 CS_PARTICLES: 'particles'}

userinfo_map={'c1': 'color1',
              'c2': 'color2',
              'tt': 'team_target',
              'hc': 'handicap',
              'c': 'country',
              'cn': 'clan',
              'so': 'spectator_only',
              't': 'team',
              'xcn': 'extended_clan',
              'tl': 'team_leader'}
