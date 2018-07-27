import discord
import random
import sys

bot = discord.Client()

def readCommandList():
    file=open('commandList.txt', 'r')
    m=""
    
    for line in file.readlines():
        m+=line
        
    return m

""" wc members in specified voice channel """
def wcMembers(targets, opts=[]):
    
    if not targets or "-help" in opts:
        m ="使用法: wc <channel ID>\n"
        m+="\n"
        m+="　--help　このヘルプを表示\n"
        return m
    
    channels=[]
    for channelID in targets:
        """ set channel """
        channel=bot.get_channel(channelID)
        
        if channel==None:
            return "Error: '%s' doesn't exist\n" % channelID
        
        elif str(channel.type)=="text":
            return "Error: '%s' is text channel\n" % channel.name
        
        channels.append(channel)
    
    m=""
    for channel in channels:
        m+="%s: %d \n" % ( channel.name, len(channel.voice_members) )
    
    return m

def startDivide(targets, opts=[]):
    
    if not targets or "-help" in opts:
        m ="使用法: roll <channel ID> [options]\n"
        m+="\n"
        m+="　　　-n　チーム数を指定\n"
        m+="　　　-u　1チームの最大人数を指定\n"
        m+="　　　　　デフォルト: -u2\n"
        m+="　--help　このヘルプを表示\n"
        return m
    
    """ initialize """
    rule=["u", 2]
    
    """ read options """
    for opt in opts:
        if opt.startswith("n") or opt.startswith("u"):
            if len(opt)==1:
                return "Error: '-%s' need number (ex: -%s3)\n" % (opt[0], opt[0])
            rule=[opt[0], int(opt[1:])]
        else:
            return "Error: unknown option '-%s'" % opt[0]
    
    channels=[]
    for channelID in targets:
        """ get channel info """
        channel=bot.get_channel(channelID)
        if channel==None:
            return "Error: '%s' doesn't exist\n" % channelID
        
        elif str(channel.type)=="text":
            return "Error: '%s' is text channel\n" % channel.name
        
        channels.append(channel)
        
    m=""
    for channel in channels:
        #channel.voice_members=["a","b","c","d","e","f","g","h","i","j"]
        if not channel.voice_members:
            m+="Warning: no one is in '%s'\n" % channel.name
        
        else:
            memberNum=len(channel.voice_members)
            if rule[0]=="u":
                teamNum=int(memberNum/rule[1]) + (memberNum%rule[1]>0)
            elif rule[0]=="n":
                teamNum=rule[1]
                
            print("  %s"       % channel.name)
            print("  %d guys"  % memberNum)
            print("  %d teams" % teamNum)
            
            random.seed()
            randomList=random.sample(channel.voice_members, memberNum)
            
            teams=[]
            for i in range(teamNum):
                teams.append( [] )
            
            for i in range(len(randomList)):
                teams[int(i%teamNum)].append( randomList[i].name )
                
            for i in range(teamNum):
                m+="#%d\n" % (i+1)
                for member in teams[i]:
                    m+="%s\n" % member
            #"""
    return m


def testCommands():
    print( parseMessage("help") )
    print( parseMessage("list") )
    print( parseMessage("roll") )
    print( parseMessage("roll --help") )
    print( parseMessage("roll 47166010791952384") )
    print( parseMessage("roll 471660107919523843") )
    print( parseMessage("roll 471660107919523845 -n") )
    print( parseMessage("roll 471660107919523845 -u") )
    print( parseMessage("roll 471660107919523845") )
    print( parseMessage("roll 471660107919523845 472022135179706368") )
    print( parseMessage("roll -n3 471660107919523845") )
    print( parseMessage("roll 471660107919523845 -n4") )
    print( parseMessage("roll 471660107919523845 -u4") )
    print( parseMessage("wc") )
    print( parseMessage("wc --help") )
    print( parseMessage("wc 47166010791952384") )
    print( parseMessage("wc 471660107919523843") )
    print( parseMessage("wc 471660107919523845") )
    print( parseMessage("wc 471660107919523845 472022135179706368") )
    
    
""" テキストを解析して、返事を生成する """
def parseMessage(content):
    print("$ %s" % content)
    
    targets=[]
    opts   =[]
    argv  =content.split(" ")
    for arg in argv[1:]:
        if arg.startswith("-"): opts.append(arg[1:])
        else:                   targets.append(arg)
    
    """ check command """
    if   argv[0]=="help" or argv[0]=="list":
        return readCommandList()
        
    elif argv[0]=="roll":
        return startDivide(targets, opts)
        
    elif argv[0]=="wc":
        return wcMembers(targets, opts)
        
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
