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

MAX_MODELS = 256
MAX_SOUNDS = 256
MAX_CLIENTS = 64
MAX_LOCATIONS = 64

# Configstring Definitions
CS_MUSIC = 2
CS_MESSAGE = 3               # from the map worldspawn's message field
CS_MOTD = 4               # g_motd string for server message of the day
CS_WARMUP = 5               # server time when the match will be restarted
CS_SCORES1 = 6
CS_SCORES2 = 7
CS_VOTE_TIME = 8
CS_VOTE_STRING = 9
CS_VOTE_YES = 10
CS_VOTE_NO = 11
CS_TEAMVOTE_TIME = 12
CS_TEAMVOTE_STRING = 14
CS_TEAMVOTE_YES = 16
CS_TEAMVOTE_NO = 18
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
