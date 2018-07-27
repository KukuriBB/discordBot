import discord
import random
import sys

bot = discord.Client()

""" count members in specified voice channel """
def countMembers(targets, opts=[]):
    print('===count===')
    
    if not targets:
        return "USAGE: count <channel ID>"
    
    channels=[]
    for channelID in targets:
        """ set channel """
        channel=bot.get_channel(channelID)
        
        if channel==None:
            return "Error: %s doesn't exist" % channelID
        
        elif str(channel.type)=="text":
            return "Error: '%s' is text channel" % channel.name
        
        channels.append(channel)
    
    m=""
    for channel in channels:
        m+="%s: %d \n" % ( channel.name, len(channel.voice_members) )
    
    return m

def startDivide(targets, opts=[]):
    print('===divide===')
    
    if not targets:
        return "USAGE: roll <channel ID> [options]"
    
    """ initialize """
    div=2
    
    """ read options """
    for opt in opts:
        """ divitions option """
        if opt.startswith("n"):
            """ check extra option """
            if len(opt)==1:
                return "Error: -n need number (ex: -n4)"
                
            div=int(opt[1:])
    
    channels=[]
    for channelID in targets:
        """ get channel info """
        channel=bot.get_channel(channelID)
        if channel==None:
            return "Error: %s doesn't exist" % channelID
        
        elif str(channel.type)=="text":
            return "Error: '%s' is text channel" % channel.name
        
        channels.append(channel)
        
    m=""
    for channel in channels:
        if not channel.voice_members:
            m+="Warning: no one is in '%s'\n" % channel.name
        
        else:
            print(channel.name)
            print("%d men a team" % div)
            
            random.seed()
            randomList=random.sample(channel.voice_members, len(channel.voice_members))
            for i in range(len(randomList)):
                m+="#" + str(int( (i+div)/div )) + " " + randomList[i].name+"\n"
                
            """
            randomList=["a","b","c","d","e","f","g","h","i","j"]
            for i in range(len(randomList)):
                m+="#" + str(int( (i+div)/div )) + " " + str(randomList[i])+"\n"
            """
    return m


def testCommands():
    print( parseMessage("roll") )
    print( parseMessage("roll 47166010791952384") )
    print( parseMessage("roll 471660107919523843") )
    print( parseMessage("roll 471660107919523845 -n") )
    print( parseMessage("roll 471660107919523845") )
    print( parseMessage("roll 471660107919523845 472022135179706368") )
    print( parseMessage("roll -n3 471660107919523845") )
    print( parseMessage("roll 471660107919523845 -n4") )
    print( parseMessage("count") )
    print( parseMessage("count 47166010791952384") )
    print( parseMessage("count 471660107919523843") )
    print( parseMessage("count 471660107919523845") )
    print( parseMessage("count 471660107919523845 472022135179706368") )
    
    
""" テキストを解析して、返事を生成する """
def parseMessage(content):
    targets=[]
    opts   =[]
    argv  =content.split(" ")
    for arg in argv[1:]:
        if arg.startswith("-"): opts.append(arg[1:])
        else:                   targets.append(arg)
    
    """ check command """
    if argv[0]=="roll":
        return startDivide(targets, opts)
        
    elif argv[0]=="count":
        return countMembers(targets, opts)
        
    return ""

""" 開始処理 """
@bot.event
async def on_ready():
    print('Logged in as')
    print("  name: %s" % bot.user.name)
    print("  id:   %s" % bot.user.id)
    #for member in bot.get_all_members():
    #testCommands()
    print('===ready===')

""" メッセージを受け取ったときに起動 """
@bot.event
async def on_message(message):
    """ ignore itself """
    if bot.user != message.author:
        """ generate reply """
        m=parseMessage(message.content)
        
        """ if valid message has been returned """
        if m!="":
            """ send message """
            await bot.send_message(message.channel, m)
        


if __name__ == '__main__':
    """ token must be specified as argv[1] """
    if len(sys.argv)!=2:
        sys.stderr.write("USAGE: python3 %s <token>\n" % sys.argv[0])
        sys.stderr.write("ex)    python3 %s NDcxNjU5MjgzNTU4MTcwNjI0.DjoTgQ.xZF_8mR26TPoCa1RFVwtkYH8B\n" % sys.argv[0])
        exit(1)
    
    """ run using specified token """
    bot.run(sys.argv[1])
