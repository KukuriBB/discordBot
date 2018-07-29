import discord
import random
import sys
import os

bot = discord.Client()
iniFile="ini/defaultSettings.txt"
ini = {}

def saveIni():
    if not os.path.isdir("ini"):
        os.makedirs("ini")
    
    file=open(iniFile, 'w')
    for key in ini.keys():
        file.write("%s:%s\n" % (key, ini[key]) )
    
    return

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
    m =readHelp( getCmd(message.content) )
    m+=readHelp( "list" )
    return m

def list(message):
    return readHelp( getCmd(message.content) )

def log(message):
    return readFile( "doc/updateLog.txt" )

""" count members in specified voice channel """
def wc(message):
    cmd, channelIDs, opts, stdin = parseContent(message.content)
    setDefault=False
    
    for opt in opts:
        if opt=="-help":
            return readHelp(cmd)
        elif opt=="-set-default":
            setDefault=True
        else:
            return "Error: unknown option '-%s'" % opt
    
    if not channelIDs:
        try:
            channelIDs.append( ini["wcDefaultChannel"] )
        except:
            return "Error: no channel was specified"
    
    if setDefault:
        if len(channelIDs)>1:
            return "Error: default channel must be unique"
        else:
            ini["wcDefaultChannel"] = channelIDs[0]
            saveIni()
            return "set default channel '%s'" % channelIDs[0]
    
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
    cmd, channelIDs, opts, members = parseContent(message.content)
    setDefault=False
    
    """ initialize """
    rule=["u", 2]
    
    for opt in opts:
        if opt=="-help":
            return readHelp(cmd)
        elif opt=="-set-default":
            setDefault=True
        elif opt.startswith("n") or opt.startswith("u"):
            if len(opt)==1:
                return "Error: '-%s' need number (ex: -%s3)\n" % (opt[0], opt[0])
            rule=[opt[0], int(opt[1:])]
        else:
            return "Error: unknown option '-%s'" % opt
    
    if (not members and not channelIDs):
        try:
            channelIDs.append( ini["rollDefaultChannel"] )
        except:
            return "Error: no channel was specified"
    
    if setDefault:
        if len(channelIDs)==0:
            return "Error: no channel was specified"
        elif len(channelIDs)>1:
            return "Error: default channel must be unique"
        else:
            ini["rollDefaultChannel"] = channelIDs[0]
            saveIni()
            return "set default channel '%s'" % channelIDs[0]
    
    """ read options """
    m=""
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
    def channelInfo(channel, l=False, d=False):
        #print( "%s\t%d\t%s\t%s" % (channel.type, channel.position, channel.id, channel.name) )
        
        m=""
        
        if channel.type==4:
            pass
        elif str(channel.type)=="text":
            pass
        elif str(channel.type)=="voice":
            pass
            

        if str(channel.type)!="voice" or d:
            m+="%s\n" % channel.name
        else:
            m+="\n%s:\n" % channel.name
            for member in channel.voice_members:
                m+="%s\n" % member.name
            m+="\n"
        
        return m
        
    cmd, channelIDs, opts, stdin = parseContent(message.content)
    
    """ show help """
    if "-help" in opts:
        return readHelp(cmd)
    
    """ initialize """
    l=False
    d=False
    
    """ read options """
    for opt in opts:
        if opt.startswith("l"):
            l=True
        elif opt.startswith("d"):
            d=True
        else:
            return "Error: unknown option '-%s'" % opt
    
    
    m=""
    channels=[]
    if channelIDs:
        for channelID in channelIDs:
            """ get channel info """
            channel=bot.get_channel(channelID)
            if channel==None:
                m+="Warning: '%s' doesn't exist\n" % channelID
            else:
                channels.append(channel)
    else:
        channels=message.server.channels
        d=True
        
    for channel in channels:
        m+=channelInfo(channel, l=l, d=d)
                    
    if m.strip()=="":
        m="none"
    
    
    return m

def test(message):
    file=open("testCmd.txt", 'r')
    
    for line in file.readlines():
        if not line.startswith("#"):
            message.content=line.strip().replace("\\n", "\n")
            
            print("==============")
            print("%s" % message.content)
            print("--------------")
            print(parseMessage(message))
    
    file.close()
    return None


""" テキストを解析して、返事を生成する """
def getCmd(content):
    return content.strip().split("\n")[0].split(" ")[0]    
    
def parseContent(content):
    text   =content.split("\n")
    argv   =text[0].strip().split(" ")
    stdin  =text[1:]
    
    cmd=argv[0]
    targets=[]
    opts   =[]
    for arg in argv[1:]:
        if arg.startswith("-"): opts.append(arg[1:])
        elif arg!=""          : targets.append(arg)
        
    
    # print("command:  %s" % cmd)
    # print("targets:  %s" % targets)
    # print("options:  %s" % opts)
    # print("stdin:    %s" % stdin)
        
    return cmd, targets, opts, stdin
    
    

def parseMessage(message):
    """ ignore itself """
    if bot.user == message.author:
        return None
        
    """ generate reply """
    cmd=getCmd(message.content)
    funcTable={
        "__cmdTest": test,
        "help": help,
        "list": list,
        "roll": roll,
        "log": log,
        "wc": wc,
        "ls": ls
    }
    
    func=funcTable.get(cmd)
    if func==None:
        return None
        
    return func(message)
    


""" 開始処理 """
@bot.event
async def on_ready():
    print('Logged in as')
    print("  name: %s" % bot.user.name)
    print("  id:   %s" % bot.user.id)
    
    try:
        file=open(iniFile , 'r')
        for line in file.readlines():
            arr=line.strip().split(":")
            ini[arr[0]]=arr[1]
        file.close()
    except:
        pass
        
    for key in ini.keys():
        print("  %s: %s" % (key, ini[key]) )
    
    print('===ready===')

""" メッセージを受け取ったときに起動 """
@bot.event
async def on_message(message):
    m=parseMessage(message)
    
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
