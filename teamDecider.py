import discord
import random

client = discord.Client()

def startDevide(content, div=2):
    m=""
    args=content.split(" ")

    if(len(args)==1):
        m+="USAGE: !roll <channel ID>"
        
    else:
        channel=client.get_channel(args[1])
        if channel==None:
            m+="Error: specified channel doesn't exist (" + args[1] + ")"
        elif str(channel.type)=="text":
            m+="Error: '" + channel.name + "' is text channel"
        elif not channel.voice_members:
            m+="Error: no member in '" + channel.name + "'"
        else:
            m+=channel.name+"\n"
            m+=str(channel.type)+"\n"
            randomList=random.sample(channel.voice_members, len(channel.voice_members))
            for i in range(len(randomList)):
                m+="#" + str(int( (i+div)/div )) + " " + randomList[i].name+"\n"
        
    m+="\n"
    
    return m

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    #for member in client.get_all_members():
    print(startDevide("!roll"))
    print(startDevide("!roll 47166010791952384"))
    print(startDevide("!roll 471660107919523843"))
    print(startDevide("!roll 471660107919523845"))
    
    print('------')

@client.event
async def on_message(message):
    # 送り主がBotだった場合反応したくないので
    if client.user != message.author:
        # 「おはよう」で始まるか調べる
        if message.content.startswith("!roll"):
            m=startDevide(message.content)
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, m)

# token にDiscordのデベロッパサイトで取得したトークンを入れてください
client.run("NDcxNjU5MjgzNTU4MTcwNjI0.DjoTgQ.xZF_8mR26TPoCa1RFVwtkYH8Bvg")
