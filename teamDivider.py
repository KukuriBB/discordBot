import discord
import random
import sys
import os
import subprocess
import numpy as np

bot = discord.Client()
iniFile="ini/defaultSettings.txt"
logFile="doc/updateLog.txt"
ini = {}
injDmTerminal="bash"
pastTeams=[]


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
    
    cmd, target, opts, stdin = parseContent(message.content)
    pastReference=False
    
    num=0
    if target:
        try:
            num=int(target[0])
        except:
            num=0
    
    for opt in opts:
        if opt=="-help":
            return readHelp(cmd)
        if opt.startswith("p"):
            pastReference=True
        else:
            return "Error: unknown option '-%s'" % opt
    
    lines=readFile( logFile )
    m=""
    
    if num==0:
        m=lines
    else:
        count=0
        for line in lines.split("\n"):
            if not line.startswith("\t"):
                count+=1
                
            if count==num:
                m+=line+"\n"
    
    return m

def injection(message):
    cmd, target, opts, stdin = parseContent(message.content)
    global injDmTerminal
    if message.author.id!="293725677960822784":
        return None
    elif message.channel.is_private:
        if cmd=="terminal":
            if len(target)!=1:
                return "Error: terminal is not specified"
            else:
                injDmTerminal=target[0]
                return "set terminal '%s'" % injDmTerminal
        terminal=injDmTerminal
        cmd=message.content
        
        
    else:
        if len(target)!=2 and target[0]!="_*":
            return None
        if not target[1].startswith("```"):
            return None
        
        terminal=target[1].strip("```")
        cmd=""
        for line in stdin[:-1]:
            cmd+=line+"\n"
    
    
    m=""
    if terminal=="python":
        dict=locals()
        exec(cmd, globals(), dict)
        m=dict["m"]
    elif terminal=="bash":
        p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        
        m+="_$ " + cmd.strip() + "_\n"
        m+=p.stdout.read().decode()
        err=p.stderr.read().decode().strip()
        if err!="":
            m+="```\n"+err+"\n```"
        m+="\n"
    return m
    
""" count members in specified voice channel """
def wc(message):
    cmd, channelIDs, opts, stdin = parseContent(message.content)
    setDefault=False
    m=""
    
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
            m+="_using default: '%s'_\n" % ini["wcDefaultChannel"]
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
        if len(channelIDs)>1:
            m+="%s: " % channel.name
        m+="%d\n" % len(channel.voice_members)
    
    return m

def roll(message):
    cmd, channelIDs, opts, members = parseContent(message.content)
    setDefault=False
    global pastTeams
    m=""
    
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
            m+="_using default: '%s'_\n" % ini["wcDefaultChannel"]
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
    
    teams=[]
    pastNum=[]
    for i in range(teamNum):
        teams.append( [] )
        pastNum.append( [] )
        
    random.shuffle(members)
    for k in range( len(members) ):
        num=-1
        for i in range( len(pastTeams) ):
            if members[k] in pastTeams[i]:
                num=i
                break
        teams[int(k%teamNum)].append( members[k] )
        pastNum[int(k%teamNum)].append( num )
    
    token=[]
    for i in range(teamNum):
        token.append( [] )
        for k in range( len(teams[i]) ):
            token[i].append( "" )
            if pastNum[i][k]>-1 and pastNum[i].count(pastNum[i][k])>=2:
                token[i][k]="**"
            print(str(i)+" "+teams[i][k]+":"+str(pastNum[i][k])+","+str( pastNum[i].count(pastNum[i][k]) ) )
            
    for i in range(teamNum):
        m+="#%d\n" % (i+1)
        for k in range( len(teams[i]) ):
            m+="　%s%s%s\n" % (token[i][k], teams[i][k], token[i][k])
    
    pastTeams=teams
    
    return m

def ls(message):
    def info(target, l=False, d=False):
        m=""
        elements=[]
        if not d and isinstance(target, discord.server.Server):
            elements=target.channels
                
        elif not d and str(target.type)=="voice":
            elements=target.voice_members
        else:
            d=True
            
            
        if not d: m+="\n"
        m+="%s" % target.name
        if not d: m+=":"
        m+="\n"
        
        for element in elements:
            m+="%s\n" % element.name
            
        return m
        
    """ initialize """
    cmd, channelIDs, opts, stdin = parseContent(message.content)
    m=""
    l=False
    d=False
    
    """ read options """
    for opt in opts:
        if opt=="-help":
            return readHelp(cmd)
        elif opt.startswith("l"):
            l=True
        elif opt.startswith("d"):
            d=True
        else:
            return "Error: unknown option '-%s'" % opt
    
    if not channelIDs:
        channelIDs.append( "." )
    
    files=[]
    dirs=[]
    for channelID in channelIDs:
        """ get info """
        channel=bot.get_channel(channelID)
        if channelID==".":
            dirs.append(message.server)
        elif channel==None:
            m+="Warning: '%s' doesn't exist\n" % channelID
        elif str(channel.type)=="voice":
            dirs.append(channel)
        else:
            files.append(channel)
    
    for file in files:
        m+=info(file, l=l, d=d)
    for dir in dirs:
        m+=info(dir,  l=l, d=d)
    
    if m.strip()=="":
        m=None
    
    
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
    if not userAccount and bot.user == message.author:
        return None
        
    """ generate reply """
    cmd=getCmd(message.content)
    funcTable={
        "_cmdTest_": test,
        "*_": injection,
        "help": help,
        "list": list,
        "roll": roll,
        "log": log,
        "wc": wc,
        "ls": ls
    }
    
    if message.channel.id=="473727730542837770":
        func=injection
    else:
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
    random.seed()
    
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
    """ if valid message has been returned """
    try:
        m=parseMessage(message)
        if m!=None and m.strip()!="":
            """ send message """
            await bot.send_message(message.channel, m)
    except:
        m ="エラー発生\n"
        m+="**```\n"+str(sys.exc_info())+"\n```**"
        await bot.send_message(message.channel, m)
        


if __name__ == '__main__':
    global userAccount
    
    """ token must be specified as argv[1] """
    if len(sys.argv)==2:
        """ run using specified token """
        userAccount=False
        bot.run(sys.argv[1])
    elif len(sys.argv)==3:
        """ run using specified token """
        userAccount=True
        bot.run(sys.argv[1], sys.argv[2])
    else:
        sys.stderr.write("USAGE: python3 %s <token>\n" % sys.argv[0])
        sys.stderr.write("ex)    python3 %s NDcxNjU5MjgzNTU4MTcwNjI0.DjoTgQ.xZF_8mR26TPoCa1RFVwtkYH8B\n" % sys.argv[0])
        exit(1)
        
