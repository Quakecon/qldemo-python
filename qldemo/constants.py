GENTITYNUM_BITS = 10
MAX_GENTITIES = 1 << GENTITYNUM_BITS
FLOAT_INT_BITS = 13
FLOAT_INT_BIAS = (1<<(FLOAT_INT_BITS-1))

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

## Trajectory Types
TR_STATIONARY=0
TR_INTERPOLATE=1
TR_LINEAR=2
TR_LINEAR_STOP=3
TR_SINE=4,
TR_GRAVITY=5

## Entity Types
ET_GENERAL=0
ET_PLAYER=1
ET_ITEM=2
ET_MISSILE=3
ET_MOVER=4
ET_BEAM=5
ET_PORTAL=6
ET_SPEAKER=7
ET_PUSH_TRIGGER=8
ET_TELEPORT_TRIGGER=9
ET_INVISIBLE=10
ET_GRAPPLE=11             # grapple hooked on wall
ET_TEAM=12
ET_EVENTS=13

## Means of Death
MOD_UNKNOWN=0
MOD_SHOTGUN=1
MOD_GAUNTLET=2
MOD_MACHINEGUN=3
MOD_GRENADE=4
MOD_GRENADE_SPLASH=5
MOD_ROCKET=6
MOD_ROCKET_SPLASH=7
MOD_PLASMA=8
MOD_PLASMA_SPLASH=9
MOD_RAILGUN=10
MOD_LIGHTNING=11
MOD_BFG=12
MOD_BFG_SPLASH=13
MOD_WATER=14
MOD_SLIME=15
MOD_LAVA=16
MOD_CRUSH=17
MOD_TELEFRAG=18
MOD_FALLING=19
MOD_SUICIDE=20
MOD_TARGET_LASER=21
MOD_TRIGGER_HURT=22
MOD_GRAPPLE=23

## Team Task
TEAMTASK_NONE=0
TEAMTASK_OFFENSE=1
TEAMTASK_DEFENSE=2
TEAMTASK_PATROL=3
TEAMTASK_FOLLOW=4
TEAMTASK_RETRIEVE=5
TEAMTASK_ESCORT=6
TEAMTASK_CAMP=7

## Team
TEAM_FREE='0'
TEAM_RED='1'
TEAM_BLUE='2'
TEAM_SPECTATOR='3'
TEAM_NUM_TEAMS='4'

TEAM_STRING_MAP={
    '0': None,
    '1': 'Red',
    '2': 'Blue',
    '3': 'Spectator'
}

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
MAX_PS_EVENTS = 2
MAX_STATS = 16
MAX_PERSISTANT = 16
MAX_POWERUPS = 16
MAX_WEAPONS = 16
MAX_MAP_AREA_BYTES = 32

# Configstring Definitions from Q3A source headers with mods for QL
CS_SERVERINFO = 0
CS_SYSTEMINFO = 1
CS_MUSIC = 2
CS_MESSAGE = 3               # from the map worldspawn's message field
CS_MOTD = 4               # g_motd string for server message of the day
CS_WARMUP = 5               # server time when the match will be restarted
CS_SCORES1 = 6
CS_SCORES2 = 7
CS_WARMUP_END = 13
CS_GAME_VERSION = 20
CS_LEVEL_START_TIME = 21   # so the timer only shows the current level
CS_INTERMISSION = 22       # when 1, fraglimit/timelimit has been hit and intermission will start in a second or two
CS_FLAGSTATUS = 23         # string indicating flag status in CTF
CS_SHADERSTATE = 24
CS_BOTINFO = 25
CS_ITEMS = 15              # string of 0's and 1's that tell which items are present
CS_MODELS = 32
CS_SOUNDS = (CS_MODELS+MAX_MODELS)
CS_PLAYERS = (CS_SOUNDS+MAX_SOUNDS)
CS_LOCATIONS = (CS_PLAYERS+MAX_CLIENTS)
CS_PARTICLES  = (CS_LOCATIONS+MAX_LOCATIONS)
CS_MAX = (CS_PARTICLES+MAX_LOCATIONS)
CS_TEAM = 659
CS_MAPCREATOR = 679

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
                 CS_PARTICLES: 'particles',
                 CS_MAPCREATOR: 'map_creator',
                 CS_WARMUP_END: 'warmup_end',
                 
}

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

