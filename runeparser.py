import json


#parseRunes() - take runesReforged.json and parses to pageIDs, runeIDs; two dicts that contain all runes associated with each 'class', and each rune associated with its ID
def parseRunes():
    f = open('runesReforged.json', 'r')
    runesReforged = json.load(f)
    f.close()

    #print(runesReforged)

    pageIDs = [] #associate each rune name to the primary/secondary ID
    runeIDs = {} #associate each rune name to the rune ID

    # search each rune in a specific class (Precision, Domination, ... )
    for i in range(0,5):
        primary_id = runesReforged[i]['id'] #get pageIDs for each class
        rune_names = [] #list for all rune names in a particular class



        #search each of the 4 rune slots in a class (Precision[0][1-4])
        for j in range(0,4):

            #search each of the (up to) 4 runes in a row (Precision[0][1-4][1-4])
            for k in range(0,5):
                try:
                    rune_name = runesReforged[i]['slots'][j]['runes'][k]['name']
                    rune_names.append(rune_name)
                    rune_id = runesReforged[i]['slots'][j]['runes'][k]['id']
                    runeIDs[rune_name] = rune_id
                except Exception as e:
                    #print("ERROR: {},{},{} -- ".format(i,j,k) + str(e))
                    continue

        #runeIDs.append(rune_page)
        pageIDs.append({primary_id:rune_names})
    return pageIDs, runeIDs

#findPageID(pageIDs, runeName) - given the dict of id:runes and the rune name, return the page id as an int
def findPageID(pageIDs, runeName):
    total_pages = len(pageIDs)
    for i in range(0,total_pages):
        key = list(pageIDs[i].keys())[0]
        for rune in pageIDs[i][key]:
            if runeName == rune:
                return int(key)


#findRuneID(runeIDs, runeName) - given the dict of runes:id and the rune name, return the id as an int
def findRuneID(runeIDs, runeName):
    return runeIDs[runeName]


def findShardID(shardIDs, shardName):
    shards = {'Adaptive Force':5008, 'Attack Speed':5005, 'Scaling CDR':5007, 'Armor':5002, 'Magic Resist':5003, 'Health':5001}
    return shards[shardName]

#example run
#pageIDs, runeIDs = parseRunes()
#primary_page = findPageID(pageIDs, "Electrocute") #returns 8100
#rune_id1 = findRuneID(runeIDs, "Predator") #returns 8124


#output files to runeIDs.txt
#f = open('runeIDs.txt', 'w+')
#f.write(json.dumps(runeIDs))
#f.write("\n\n")
#f.write(json.dumps(pageIDs))
#f.close()
