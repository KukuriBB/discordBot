import discord
import random

bot = discord.Client()

def countMembers(content):
    channelID=""
    
    # read argments
    for arg in content.split(" ")[1:]:
        # get channel
        channelID=arg
            
    
    if(channelID==""):
        return "USAGE: !count <channel ID>"
    
    # get channel info
    channel=bot.get_channel(channelID)
    if channel==None:
        return "Error: %s doesn't exist" % arg
    
    elif str(channel.type)=="text":
        return "Error: '" + channel.name + "' is text channel"
        
    return "%d" % len(channel.voice_members)


def startDevide(content):
    channelID=""
    div=2
    
    # read argments
    for arg in content.split(" ")[1:]:
        # divitions option
        if arg.startswith("-n"):
            # check extra option
            if len(arg)==2:
                return "Error: -n need number (ex: -n4)"
                
            div=int(arg[2:])
        else:
            # get channel
            channelID=arg
            #channelID=bot.get_channel(arg)
            
    
    if(channelID==""):
        return "USAGE: !roll <channel ID> [options]"
    
    # get channel info
    channel=bot.get_channel(channelID)
    if channel==None:
        return "Error: %s doesn't exist" % arg
    
    elif str(channel.type)=="text":
        return "Error: '" + channel.name + "' is text channel"
        
    elif not channel.voice_members:
        return "Error: no one is in '" + channel.name + "'"
        
    else:
        print(channel.name)
        print("%d men in team" % div)
        
        randomList=random.sample(channel.voice_members, len(channel.voice_members))
        m=""
        for i in range(len(randomList)):
            m+="#" + str(int( (i+div)/div )) + " " + randomList[i].name+"\n"
    
    return m


def testCommands():
    print( startDevide("!roll") )
    print( startDevide("!roll 47166010791952384") )
    print( startDevide("!roll 471660107919523843") )
    print( startDevide("!roll 471660107919523845 -n") )
    print( startDevide("!roll 471660107919523845") )
    print( startDevide("!roll -n3 471660107919523845") )
    print( startDevide("!roll 471660107919523845 -n4") )
    print( countMembers("!count") )
    print( countMembers("!count 47166010791952384") )
    print( countMembers("!count 471660107919523843") )
    print( countMembers("!count 471660107919523845") )


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    #for member in bot.get_all_members():
    #testCommands()
    print('===ready===')

@bot.event
async def on_message(message):
    # ignore itself
    if bot.user != message.author:   
        # check command
        if message.content.startswith("!roll"):
            print('===devide===')
            m=startDevide(message.content)
            await bot.send_message(message.channel, m)
        elif message.content.startswith("!wc"):
            print('===count===')
            m=countMembers(message.content)
            await bot.send_message(message.channel, m)

# token にDiscordのデベロッパサイトで取得したトークンを入れてください
bot.run("NDcxNjU5MjgzNTU4MTcwNjI0.DjoTgQ.xZF_8mR26TPoCa1RFVwtkYH8Bvg")
