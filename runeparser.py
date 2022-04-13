import json

def parseRunes():
    f = open('runesReforged.json', 'r')
    runesReforged = json.load(f)
    f.close()

    #print(runesReforged)

    pageIDs = [] #associate each rune name to the primary/secondary ID
    runeIDs = {} #associate each rune name to the rune ID

    # search each rune in a specific class (Precision, Domination, ... )
    for i in range(0,4):
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
                    print("ERROR: {},{},{} -- ".format(i,j,k) + str(e))
                    #print(str(i) + "," + str(j) + "," + str(k) + " does not exist!")
                    #continue

        #runeIDs.append(rune_page)
        pageIDs.append({primary_id:rune_names})
    return pageIDs, runeIDs

pageIDs, runeIDs = parseRunes()

#print(runeIDs)
f = open('runeIDs.txt', 'w+')
f.write(json.dumps(runeIDs))
f.write("\n")
f.write(json.dumps(pageIDs))
f.close()

def findPrimaryPage(runeName):
    pass
