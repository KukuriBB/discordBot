import discord
import random
import sys

bot = discord.Client()
commandListFile="commandList.txt"

""" read file """
def readFile(fileName):
    file=open(fileName, 'r')
    m=""
    
    for line in file.readlines():
        m+=line
    
    file.close()
    return m
    
def readHelp( cmd ):
    return readFile( "doc/reference_%s.txt" % cmd )
    
def help(message):
    return readHelp( getCmd(message) )

def list(message):
    return readHelp( getCmd(message) )

""" count members in specified voice channel """
def wc(message):
    cmd, channelIDs, opts, stdin = parseMessage(message)
    
    if not channelIDs or "-help" in opts:
        return readHelp(cmd)
    
    channels=[]
    m=""
    for channelID in channelIDs:
        """ set channel """
        channel=bot.get_channel(channelID)
        
        if channel==None:
            m+="Warning: '%s' doesn't exist\n" % channelID
        
        elif str(channel.type)=="text":
            m+="Warning: '%s' is text channel\n" % channel.name
        
        else:
            channels.append(channel)
    
    for channel in channels:
        m+="%s: %d \n" % ( channel.name, len(channel.voice_members) )
    
    return m

def roll(message):
    cmd, channelIDs, opts, members = parseMessage(message)
    
    """ show help """
    if (not members and not channelIDs) or "-help" in opts:
        return readHelp(cmd)
    
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
    
    m=""
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
            
            elif not channel.voice_members:
                m+="Warning: no one is in '%s'\n" % channel.name
            
            else:
                for voice_member in channel.voice_members:
                    members.append( voice_member.name )
    
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
        teams[int(i%teamNum)].append( members[i] )
        
    for i in range(teamNum):
        m+="#%d\n" % (i+1)
        for member in teams[i]:
            m+="　%s\n" % member
    
    return m


def ls(message):
    cmd, channelIDs, opts, stdin = parseMessage(message)
    
    """ show help """
    if "-help" in opts:
        return readHelp(cmd)
    
    """ initialize """
    l=0
    d=0
    
    """ read options """
    for opt in opts:
        if opt.startswith("l"):
            l=1
        elif opt.startswith("d"):
            d=1
        else:
            return "Error: unknown option '-%s'" % opt[0]
    
    
    m=""
    targets=[]
    if channelIDs:
        for channelID in channelIDs:
            """ get channel info """
            channel=bot.get_channel(channelID)
            if channel==None:
                m+="Warning: '%s' doesn't exist\n" % channelID
            else:
                targets.append(channel)
    else:
        targets.append(message.server)
        
    for target in targets:
        if isinstance( target, discord.server.Server ):
            for channel in target.channels:
                m+="%s\n" % channel.name
        else:
            if target.type==4:
                m+="%s\n" % target.name
                
            elif str(target.type)=="text":
                m+="%s\n" % target.name
            
            elif str(target.type)=="voice":
                if d==0:
                    if len(targets)>1:
                        m+="%s:\n" % target.name
                        indent="  "
                    else:
                        indent=""
                        
                    for member in target.voice_members:
                        m+="%s%s\n" % (indent, member.name)
                    m+="\n"
                else:
                    m+="%s\n" % target.name
                    
    if m.strip()=="":
        m="none"
    
    
    return m



""" テキストを解析して、返事を生成する """
def getCmd(message):
    return message.content.strip().split(" ")[0]    
    
def parseMessage(message):
    text   =message.content.split("\n")
    argv   =text[0].strip().split(" ")
    
    cmd=argv[0]
    targets=[]
    opts   =[]
    for arg in argv[1:]:
        if arg.startswith("-"): opts.append(arg[1:])
        elif arg!=""          : targets.append(arg)
        
    stdin  =text[1:]
    
    print("==============")
    print("command:  %s" % cmd)
    print("targets:  %s" % targets)
    print("options:  %s" % opts)
    print("stdin:    %s" % stdin)
    print("--------------")
        
    return cmd, targets, opts, stdin
    
    


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
        cmd=getCmd(message)
        funcTable={
            "help": help,
            "list": list,
            "roll": roll,
            "wc": wc,
            "ls": ls
        }
        
        m=None
        func=funcTable.get(cmd)
        if func!=None:
            m=func(message)
        
        """ if valid message has been returned """
        if m!=None:
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
