# Steam-Games-in-Common

This can be used to get steam games that are shared between any number of steam accounts.

#### NOTE:

In order to use either method, you must edit  the file SteamWebAPI and enter your steam webapi key.  
If you do not already have one, you get receive an api key from [https://steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey) .

## Use Method #1: Steam ID

``` python
steamidlist = ['76561197997457199','76561198022367213','76561198041510733']      
percentCutoff = 100      
gamelist = findGamesInCommon(percentCutoff, steamidlist)  

```

Alternatively,

``` python
gamelist = findGamesInCommon(65, '76561197997457199','76561198022367213','76561198041510733')  

```

## Use Method #2: Discord ID

Copy the discord ID's of the users you want,  
![Right-click a discord user and click copy id to copy their discord id to your clipboard.](https://i.imgur.com/MbYZ3ZI.png)  
and in discordSteamIDlink.json put in their discord id linked to thier steam id in this format:

``` JSON
{      
  "userIDs":      
  {      
    "DISCORDXXXXXXXXXXX":"STEAMIDXXXXXXXXXX",      
    "227581562345095168":"76561198022367213"      
  }      
}  

```

Finally, you can call `pullGamesInCommonFromDiscordIDs` with a number from 0-100 and either a list of the ids (see the file for this example) or with arguments of the discord ids as strings.

``` python
mentionedIDList = ['227581562345095168','112973823447470080','105055491113099264']    
percentCutoff = 75    
gamelist = pullGamesInCommonFromDiscordIDs(percentCutoff,mentionedIDList)  

```

Alternatively:

``` python
gamelist = pullGamesInCommonFromDiscordIDs(100,['227581562345095168','112973823447470080','105055491113099264'])  

```

## Discord-py example:

```python
    @commands.command(pass_context=True, no_pm=True)  
    async def game(self, ctx):  
        """Lists games in common"""  
  
        mentionedUsersSteamIDs = []  
        mentionIDList = []  
  
        mentionList = ctx.message.mentions  
        for member in mentionList:  
            mentionIDList.append(str(member.id))  
  
        from steamgamesv2 import pullGamesInCommonFromDiscordIDs
        game = pullGamesInCommonFromDiscordIDs(100,mentionIDList)  
        games = str(game).replace('\'', '').strip('[').strip(']')  
        for x in range(0,int(len(games)/1998)+1):  
            #print(str(games)[x*2000:(x+1)*2000])  
            await self.bot.say('`' + games[x*1998:(x+1)*1998] + '`')  

```
