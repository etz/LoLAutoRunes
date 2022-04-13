import requests
import base64
import json
import time

from runescraper import *
from runeparser import *


###################   API Data   #######################
#parseLockFileWin(path=r"") - takes an absolute path to parse lockfile, otherwise check common install locations. returns port, b'password'
def parseLockFileWin(path=r""):
    if path != r"":
        try:
            with open(drive+location, 'r') as f:
                lockfile = f.readline()
                lockfile = lockfile.split(':')
                return lockfile[2], bytes(lockfile[3], 'utf-8') #return port, password
        except:
            print("Installation location not found" + drive + location)
            return 0 #if location does not work
    user_drives = [r'C:',r'D:',r'E:',r'F:']
    install_locations = [r'\Riot Games\League of Legends\lockfile', r'\Program Files\Riot Games\League of Legends\lockfile', r'\Program Files (x86)\Riot Games\League of Legends\lockfile']
    for drive in user_drives:
        for location in install_locations:
            try:
                with open(drive+location, 'r') as f:
                    lockfile = f.readline()
                    lockfile = lockfile.split(':')
                    return lockfile[2], bytes(lockfile[3], 'utf-8') #return port, password
            except:
                print("Installation is not located at: " + drive + location)
    return 0 #if location not found

#parseLockFileMac(path=r"") - takes an absolute path to parse lockfile, otherwise check common install locations. returns port, b'password'
def parseLockFileMac(path=r""):
    pass

#parseAPIData(port, password) - takes port, b'password' and parses LCU API data
def parseAPIData(port, password):
    API = 'https://127.0.0.1:' + str(port)
    auth = 'Basic ' + base64.b64encode(b'riot:' + password).decode('utf-8')
    header = {'Authorization' : auth}
    return API, auth, header

###################   Champion Data   #######################
#getCurrentChampionID(API, header): Returns ID for the champion locked in; returns int
def getCurrentChampionID(API, header):
    get_champion_id = API + "/lol-champ-select/v1/current-champion" #returns 404 if not selected, 200 if so
    r = requests.get(get_champion_id, headers=header, verify=False)
    while(r.status_code != 200 or r.json() == 0):
        time.sleep(3)
        r = requests.get(get_champion_id, headers=header, verify=False)
    get_champion_id = r.json()
    return get_champion_id

#getCurrentChampionName(API, header): Returns Name for the champion locked in; returns str
def getCurrentChampionName(API, header):
    current_champ_id = getCurrentChampionID(API, header)
    get_champion_name = API + "/lol-champ-select/v1/grid-champions/" + str(current_champ_id)
    r = requests.get(get_champion_name, headers=header, verify=False)
    get_champion_name = r.json()
    return get_champion_name['name']

###################   Rune Page Data   #######################
#setNewRunePage(API, header, champion, primary, secondary, runes=[], current="true"); returns success or error
def setNewRunePage(API, header, gamemode, champion, primary, secondary, runes=[], current="true"):
    print("Creating new page for " + champion)
    gamemode = "{} {}".format(gamemode.capitalize(), champion)
    if len(gamemode) > 25:
        gamemode = gamemode[0:24]
    new_page = json.dumps({"name":gamemode, "primaryStyleId":primary, "subStyleId":secondary, "selectedPerkIds": runes, "current":"{}".format(current) })
    set_page = API + '/lol-perks/v1/pages'
    r = requests.post(set_page, headers=header, verify=False, data=new_page) #returns 200
    if(r.status_code != 200):
        print("Error generating new page, is there already maximum rune pages?")
    else:
        print("Success")

#getCurrentRunePage(API, header); returns current rune page ID
def getCurrentRunePage(API, header):
    #get current rune page id
    get_current_page = API + '/lol-perks/v1/currentpage'
    r = requests.get(get_current_page, headers=header, verify=False) #returns 200
    current_page = r.json()
    return str(current_page['id'])

#getCurrentRunePage(API, header); returns nothing, deletes the current rune page
def deleteCurrentRunePage(API, header):
    #define current rune page and put into current_page
    current_page = getCurrentRunePage(API, header)
    #delete current rune page by ID
    del_current_page = API + '/lol-perks/v1/pages/' + current_page
    r = requests.delete(del_current_page, headers=header, verify=False) #returns 204

#deleteRunePage(API, header, page); returns nothing, deletes a specific rune page based on ID
def deleteRunePage(API, header, pageID):
    #delete current rune page by ID
    del_page = API + '/lol-perks/v1/pages/' + pageID
    r = requests.delete(del_page, headers=header, verify=False) #returns 204

def getRunePages(API, header):
    pass

###################   Lobby Data   #######################
def getGameMode(API, header):
    get_game_mode = API + '/lol-lobby/v2/lobby'
    r = requests.get(get_game_mode, headers=header, verify=False) #returns 200
    r = r.json()
    return r['gameConfig']['gameMode']



# Main function

"""Connect to LCU API"""
port, password = parseLockFileWin()
API, auth, header = parseAPIData(port, password)

"""Get current client version"""
#TBD

"""Check against downloaded runesReforged.json"""
#TBD

"""Parse runesReforged.json"""
pageIDs, runeIDs = parseRunes('12.7.1-runesReforged.json') #Add auto-updater

"""Determine if in match"""

"""Determine gamemode"""
gamemode = getGameMode(API, header)


"""Determine selected champion"""
champion_name = getCurrentChampionName(API, header)
champion = ""
for char in champion_name:
    if char.isalpha():
        champion += char

"""Fetch runes"""
runes, shards = getRunesUGG(champion, gamemode)

"""Parse rune names to ids"""
rune_ids = nameToID(runes,shards)

"""Get primary and sub ids"""
primary = findPageID(pageIDs, runes[0])
secondary = findPageID(pageIDs, runes[5])

"""Delete current rune page"""
deleteCurrentRunePage(API, header)

"""Create new rune page with fetched runes"""
setNewRunePage(API, header, gamemode, champion_name, primary, secondary, rune_ids, current="true")
