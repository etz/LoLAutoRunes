import requests
import base64

#define these from user client
password = b"Oj0rXeMWm9CbgfvNRIrweg"
port = 55886

#prepare LCU connection
API = 'https://127.0.0.1:' + str(port)
auth = 'Basic ' + base64.b64encode(b'riot:' + password).decode('utf-8')
header = {'Authorization' : auth}

#get summoner information; returns status 200
summoner = API + '/lol-summoner/v1/current-summoner'
r = requests.get(summoner, headers=header, verify=False)

def setNewPage():


def deleteCurrentPage(API, headers):
    #define current rune page and put into current_page; returns status 200
    get_current_page = API + '/lol-perks/v1/currentpage'
    r = requests.get(get_current_page, headers=header, verify=False)
    current_page = r.json()
    #delete current rune page by ID
    del_current_page = API + '/lol-perks/v1/pages/' + str(current_page['id'])
    r = requests.delete(del_current_page, headers=header, verify=False)

#print(r.status_code) #204
#print(r.headers)

# Accessing the LCU API


deleteCurrentPage(API, headers)
