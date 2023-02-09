from urllib.request import urlopen
import json, os, re

def getSteamWebAPIID ():
    cwd = os.getcwd()
    with open (cwd + '\SteamWebAPI') as apifile:
        data = apifile.readlines()
        return re.sub(r'\W+', '', data[0])

def getSteamLibrary(*steamids):
    superIDDict = {} #dict of all games in all libraries
    superIDLogoDict = {} #dict of all game logos in all libraries
    games = []
    formatedgames = [] #list of lists of games in each library

    user = 0
    for steamid in steamids:
        url = ('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + str(getSteamWebAPIID()) + '&steamid=' + str(steamid) + '&include_appinfo=1&include_played_free_games=1&format=json')
        document = urlopen(url)
        tree = json.load(document)
        idlist = []
        for _message in tree["response"]["games"]:
            idlist.append(int(_message["appid"]))
            superIDDict[_message["name"]] = int(_message["appid"])
            superIDLogoDict[int(_message["appid"])] = _message["img_icon_url"]

        sortedids = sorted(idlist, key=int)
        games.append([user,sortedids])
        user += 1

    import operator #sort dict by value
    superIDDict = sorted(superIDDict.items(),key=operator.itemgetter(1))


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

        formatedgames.append(childgames)
    return [formatedgames, superIDDict, superIDLogoDict]

def findGamesInCommon(percentCutoff,*steamids):
    libraries = getSteamLibrary(*steamids) #returns [formatedgames, superIDDict, superIDLogoDict]
    playergames = libraries[0] #list of lists of games in each library
    superid = libraries[1] #dict of all games in all libraries

    gameNameListIncommon = [] #list of games in common

    cutoff = percentCutoff/100 #convert percent to decimal
    gameIDsThatPassCutoff = [] #list of games that pass the cutoff

    gamesInCommonPercentage = [None] * (len(superid)) #list of percentages of games in common
    gamesInCommonCount = [] #list of counts of games in common
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

        name = gameIDsThatPassCutoff[count][0]
        gameNameListIncommon.append(name)

    return gameNameListIncommon

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
