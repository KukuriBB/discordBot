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

""" count members in specified voice channel """
def wc(channelIDs, opts=[], stdin=[]):
    m=""
    
    if not channelIDs or "-help" in opts:
        m ="使用法: wc <channel ID>\n"
        m+="\n"
        m+="　--help　このヘルプを表示\n"
        return m
    
    channels=[]
    for channelID in channelIDs:
        """ set channel """
        channel=bot.get_channel(channelID)
        
        if channel==None:
            m+="Warning: '%s' doesn't exist\n" % channelID
        
        elif str(channel.type)=="text":
            m+="Warning: '%s' is text channel\n" % channel.name
        
        channels.append(channel)
    
    for channel in channels:
        m+="%s: %d \n" % ( channel.name, len(channel.voice_members) )
    
    return m

def roll(channelIDs, opts=[], members=[]):
    m=""
    
    if (not members and not channelIDs) or "-help" in opts:
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
    
    #members=["a","b","c","d","e","f","g","h","i","j"]
    if not members:
        channels=[]
        for channelID in channelIDs:
            """ get channel info """
            channel=bot.get_channel(channelID)
            if channel==None:
                m+="Warning: '%s' doesn't exist\n" % channelID
            
            elif str(channel.type)=="text":
                m+="Warning: '%s' is text channel\n" % channel.name
            
            if not channel.voice_members:
                m+="Warning: no one is in '%s'\n" % channel.name
            
            else:
                members.extend(channel.voice_members)
    
    memberNum=len(members)
    if rule[0]=="u":
        teamNum=int(memberNum/rule[1]) + (memberNum%rule[1]>0)
    elif rule[0]=="n":
        teamNum=rule[1]
        
    print("  %d guys"  % memberNum)
    print("  %d teams" % teamNum)
    
    random.seed()
    random.shuffle(members)
    
    teams=[]
    for i in range(teamNum):
        teams.append( [] )
    
    for i in range(len(members)):
        #teams[int(i%teamNum)].append( members[i].name )
        teams[int(i%teamNum)].append( str(members[i]) )
        
    for i in range(teamNum):
        m+="#%d\n" % (i+1)
        for member in teams[i]:
            m+="　%s\n" % member
    
    return m


def testCommands():
    print( parseMessage("cmd file1 file2 -n2 -u4\nhoge\nfuga\npya") )
    print( parseMessage("help") )
    print( parseMessage("list") )
    print( parseMessage("roll") )
    print( parseMessage("roll --help") )
    print( parseMessage("roll 47166010791952384") )
    print( parseMessage("roll 471660107919523843") )
    print( parseMessage("roll 471660107919523845 -n") )
    print( parseMessage("roll 471660107919523845 -u") )
    print( parseMessage("roll 471660107919523845") )
    print( parseMessage("roll 471660107919523845 -n4") )
    print( parseMessage("roll 471660107919523845 -u4") )
    print( parseMessage("roll 471660107919523845 472022135179706368") )
    print( parseMessage("roll 471660107919523845\nhoge\nfuga\npya\nfoo\nbar\nyo\nne\nmo\nto") )
    print( parseMessage("wc") )
    print( parseMessage("wc --help") )
    print( parseMessage("wc 47166010791952384") )
    print( parseMessage("wc 471660107919523843") )
    print( parseMessage("wc 471660107919523845") )
    print( parseMessage("wc 471660107919523845 472022135179706368") )
    
    
""" テキストを解析して、返事を生成する """
def parseMessage(content):
    content=content.split("\n")
    
    argv   =content[0].split(" ")
    stdin  =content[1:]
    
    cmd=argv[0]
    targets=[]
    opts   =[]
    for arg in argv[1:]:
        if arg.startswith("-"): opts.append(arg[1:])
        else:                   targets.append(arg)
    
    print("cmd:      %s" % cmd)
    print("targets:  %s" % targets)
    print("options:  %s" % opts)
    print("stdin:    %s" % stdin)
    
    
    """ check command """
    if   cmd=="help" or cmd=="list":
        return readCommandList()
        
    elif cmd=="roll":
        return roll(targets, opts, stdin)
        
    elif cmd=="wc":
        return wc(targets, opts)
        
    return ""

""" 開始処理 """
@bot.event
async def on_ready():
    print('Logged in as')
    print("  name: %s" % bot.user.name)
    print("  id:   %s" % bot.user.id)
    #for member in bot.get_all_members():
    testCommands()
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
