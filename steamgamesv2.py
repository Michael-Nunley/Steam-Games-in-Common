from urllib.request import urlopen
import json, os, re

def getSteamWebAPIID ():
    cwd = os.getcwd()
    with open (cwd + '\SteamWebAPI') as apifile:
        data = apifile.readlines()
        return re.sub(r'\W+', '', data[0])

def getSteamLibrary(*steamids):
    superIDDictu = {}
    superIDDict = {}
    superIDLogoDictu = {}
    superIDLogoDict = {}
    games = []
    formatedgames = []

    user = 0
    for steamid in steamids:
        url = ('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + str(getSteamWebAPIID()) + '&steamid=' + str(steamid) + '&include_appinfo=1&include_played_free_games=1&format=json')
        document = urlopen(url)
        tree = json.load(document)
        idlist = []
        for _message in tree["response"]["games"]:
            idlist.append(int(_message["appid"]))
            superIDDictu[_message["name"]] = int(_message["appid"])
            superIDLogoDictu[int(_message["appid"])] = _message["img_icon_url"]

        sortedids = sorted(idlist, key=int)
        games.append([user,sortedids])
        user += 1

    import operator
    superIDDict = sorted(superIDDictu.items(),key=operator.itemgetter(1))


    childcount = 0
    for child in games:
        childgames = []
        for gameid in superIDDict:
            duplicates = 0

            for childgameid in child[1]:
                if childgameid == gameid[1]:
                    duplicates = 1

            if duplicates == 1:
                childgames.append(gameid[1])
            else:
                childgames.append(None)

        childcount += 1
        formatedgames.append(childgames)
    returnobject = [formatedgames, superIDDict, superIDLogoDict]
    return returnobject

def findGamesInCommon(percentCutoff,*steamids):
    libraries = getSteamLibrary(*steamids)
    playergames = libraries[0]
    superid = libraries[1]

    gameNameListIncommon = []

    cutoff = percentCutoff/100
    gameIDsThatPassCutoff = []

    gamesInCommonPercentage = [None] * (len(superid))
    gamesInCommonCount = []
    for x in range(0,(len(superid))):
        gamesInCommonCount.append(int(0))

    for person in range(len(playergames)):
        for gameid in range(len(superid)):
            if superid[gameid][1] == playergames[person][gameid]:
                gamesInCommonCount[gameid] = int(gamesInCommonCount[gameid] + 1)

    for count in range(len(gamesInCommonCount)):
        gamesInCommonPercentage[count] = gamesInCommonCount[count]/max(gamesInCommonCount)
        if ((gamesInCommonCount[count]/max(gamesInCommonCount)) >= cutoff):
            gameIDsThatPassCutoff.append(superid[count])

    for _id in gameIDsThatPassCutoff:
        name = _id[0]
        gameNameListIncommon.append(name)

    return gameNameListIncommon
    #return gameIDsThatPassCutoff

def pullGamesInCommonFromDiscordIDs(percentCutoff,*mentionIDs):
    steamIDS = []
    steamIDS = getSteamIDfromDiscordID(*mentionIDs)
    return findGamesInCommon(percentCutoff,*steamIDS)


def getSteamIDfromDiscordID(*mentionIDs):
    steamIDs = []

    mdata = []
    cwd = os.getcwd()
    with open(cwd + '\discordSteamIDlink.json') as json_data:
        d = json.load(json_data)
        mdata = d["userIDs"]

    for mention in mentionIDs[0]:
        steamIDs.append(mdata[mention])

    return steamIDs

mentionedIDList = ['227581562345095168','112973823447470080','105055491113099264']
games = pullGamesInCommonFromDiscordIDs(100,mentionedIDList)
print(games)
