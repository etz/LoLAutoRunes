import requests
import base64
import json
import time

from runescraper import *
from runeparser import *


#define these from user client <lockfile or process list>
password = b"0tbIC9ZD5ln58mnxTaYBIw"
port = 61857

#prepare LCU connection
API = 'https://127.0.0.1:' + str(port)
auth = 'Basic ' + base64.b64encode(b'riot:' + password).decode('utf-8')
header = {'Authorization' : auth}




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
def setNewRunePage(API, header, champion, primary, secondary, runes=[], current="true"):
    print("Creating new page for " + champion)
    new_page = json.dumps({"name":"AR {}".format(champion), "primaryStyleId":primary, "subStyleId":secondary, "selectedPerkIds": runes, "current":"{}".format(current) })
    set_page = API + '/lol-perks/v1/pages'
    r = requests.post(set_page, headers=header, verify=False, data=new_page) #returns 200
    if(r.status_code != 200):
        print("Error generating new page, is there already maximum rune pages?")
        pass
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



# Main function

"""Parse runesReforged.json"""
pageIDs, runeIDs = parseRunes()
"""Determine if in match"""

"""Determine gamemode"""
gamemode = "rift"
"""Determine selected champion"""
champion = getCurrentChampionName(API, header)
"""Fetch runes"""
runes, shards = getRunesUGG(champion, gamemode)
"""Parse rune names to ids"""
rune_ids = []

for i in range(0,len(runes)):
    rune = findRuneID(runeIDs, runes[i])
    rune_ids.append(rune)

for i in range(0,len(shards)):
    shard = findShardID(runeIDs, shards[i])
    rune_ids.append(shard)

print(rune_ids)

"""Get primary and sub ids"""
primary = findPageID(pageIDs, runes[0])
secondary = findPageID(pageIDs, runes[5])
"""Delete current rune page"""
deleteCurrentRunePage(API, header)
"""Create new rune page with fetched runes"""
setNewRunePage(API, header, champion, primary, secondary, rune_ids, current="true")
