import requests
import base64
import json
import time

#define these from user client <lockfile or process list>
password = b"Oj0rXeMWm9CbgfvNRIrweg"
port = 55886

#prepare LCU connection
API = 'https://127.0.0.1:' + str(port)
auth = 'Basic ' + base64.b64encode(b'riot:' + password).decode('utf-8')
header = {'Authorization' : auth}

#get summoner information; returns status 200
summoner = API + '/lol-summoner/v1/current-summoner'
r = requests.get(summoner, headers=header, verify=False)

#new rune page data <get from u.gg/op.gg/etc>
champion = "Tukong"
primary = 8300
secondary = 8400
runes = [8351,8313,8345,8347,8451,8444,5007,5002,5001]
current = "true"


def getCurrentChampion(API, header):
    get_champion = API + "/lol-champ-select/v1/current-champion" #returns 404 if not selected, 200 if so
    r = requests.get(get_champion, headers=header, verify=False)
    while(r.status_code != 200):
        time.sleep(5)
    pass

def setNewPage(API, header, champion, primary, secondary, runes=[], current="true"):
    print("Creating new page for " + champion)
    new_page = json.dumps({"name":"{}".format(champion), "primaryStyleId":primary, "subStyleId":secondary, "selectedPerkIds": runes, "current":"{}".format(current) })
    set_page = API + '/lol-perks/v1/pages'
    r = requests.post(set_page, headers=header, verify=False, data=new_page) #returns 200
    if(r.status_code != 200):
        print("Error generating new page, is there already maximum rune pages?")

def getCurrentPage(API, header):
    #get current rune page id
    get_current_page = API + '/lol-perks/v1/currentpage'
    r = requests.get(get_current_page, headers=header, verify=False) #returns 200
    current_page = r.json()
    return str(current_page['id'])

def deleteCurrentPage(API, header):
    #define current rune page and put into current_page
    current_page = getCurrentPage(API, header)
    #delete current rune page by ID
    del_current_page = API + '/lol-perks/v1/pages/' + current_page
    r = requests.delete(del_current_page, headers=header, verify=False) #returns 204

# Accessing the LCU API


getCurrentPage(API, header)
deleteCurrentPage(API, header)
setNewPage(API, header, champion, primary, secondary, runes, current)
