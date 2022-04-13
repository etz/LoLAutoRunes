from bs4 import BeautifulSoup
import requests


#u.gg rune scraper

#gamemode not implemented yet
def getRunesUGG(champion, gamemode):
    runes = [] #6 runes
    shards = [] #3 shards

    #get u.gg runes page
    URL = 'https://u.gg/lol/champions/' + champion + '/build'
    r = requests.get(URL)

    if r.status_code != 200:
        print("There was an error getting the u.gg data associated with: " + champion)
        return 0, 0

    soup = BeautifulSoup(r.text, 'html.parser')

    #get runes
    for div in soup.find_all('div', 'perk-active'):
        for img in div.find_all('img', alt=True):
            if img['alt'] in runes:
                continue
            else:
                runes.append(img['alt'])

    #get shards
    for div in soup.find_all('div', 'shard-active'):
        for img in div.find_all('img', alt=True):
            if len(shards) >= 3:
                continue
            else:
                shards.append(img['alt'])

    #rune text manipulation
    for i in range(0,len(runes)):
        if 'Keystone' in runes[i]:
            runes[i] = runes[i][13:]
        else:
            runes[i] = runes[i][9:]

    #shard text manipulation
    for i in range(0,len(shards)):
        shards[i] = shards[i][4:-6]


    return runes, shards



runes, shards = getRunesUGG('illaoi', 'rift')
print(runes)
print(shards)
