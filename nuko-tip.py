import discord
import json
import os
import fnmatch
from web3 import Web3,HTTPProvider

keystoredir = "/home/pi/.nekonium/keystore"
bottoken = 'Mzk5OTI0NjkyMTQxNjA0ODc1.DTUKtg.X-kVvDhrx3GNJgUaawnFY6wkDTU'

print(discord.__version__)
web3 = Web3(HTTPProvider('http://localhost:8293'))

balancecomm = ["!manekinuko","balance"]
mkwalletcomm = ["!manekinuko","mkwallet","password","password"]
getkeycomm = ["!manekinuko","getkey"]
tippingcomm = ["!manekinuko","tip","@foo","value"]
unlockcomm = ["!manekinuko","unlock","password"]
helpcomm = ["!manekinuko","help"]
whataddcomm = ["!manekinuko","whatadd", "@foo"]

def balance(user_name):
    saydata = "error"
    #アドレス帳読み込み
    with open("add_dict.json",'r') as f:
        address_dict = json.load(f)
    #アドレス帳内にすでにアドレスがあるか確認
    ##あった
    if(user_name in address_dict) == True:
        print(address_dict[user_name])
        saydata = user_name + " ,address:\n[" + address_dict[user_name] + "]\n\n" + "balance:" + str(web3.fromWei(web3.eth.getBalance(address_dict[user_name]),"ether")) + " nuko"
    ##なかった
    else:
        saydata = "Not Find Your address"
    print(user_name)#デバッグ用
    return saydata 

def mkwallet(user_name, pasword):
    #アドレス読み込み
    with open("add_dict.json",'r') as f:
        address_dict = json.load(f)
    #すでにアドレス持ってるかの確認
    ##持ってない
    if (user_name in address_dict) == False:
        address = "test address"
        address = web3.personal.newAccount(pasword)
        address_dict[user_name] = address
        #アドレス帳書き込み
        with open("add_dict.json",'w') as f:
            json.dump(address_dict,f)
        state = user_name + ", Your address:\n[" + address_dict[user_name] + "]\n\n" + "password:[" + pasword + "]. "

    ##持ってる
    else:
        state = user_name + "You have address. "

    print(user_name)
    state = state
    return state

def pkey(user_name):
    keyname = "error"
    with open("add_dict.json",'r') as f:
        address_dict = json.load(f)

    hint = "*"+(address_dict[user_name].lstrip("0x"))
    print(hint)

    for filename in os.listdir(keystoredir):
        if fnmatch.fnmatch(filename,hint):
            keyname = filename
    print(keyname)
    return keyname

def tipping(user_name, user_name2, value):
    #アドレス読み込み
    with open("add_dict.json",'r') as f:
        address_dict = json.load(f)
    #アドレス確認
    if ((user_name in address_dict) == True) and ((user_name2 in address_dict) == True):
        state = "tip\nfrom:[" + address_dict[user_name] + "]\nto:[" + address_dict[user_name2] + "], \nvalue:" + str(value) + " nuko\n"
        unlock =  True#web3.personal.unlockAccount(address_dict[user_name],"test")
        if unlock == True:
            trans = web3.eth.sendTransaction({"to": address_dict[user_name2], "from": address_dict[user_name], "value": web3.toWei(value,"ether")})
            state = state + "unlock true\n"
            state = state + "trans:" + trans + "\n"
        else:
            state = state + "unlock error\n"
    else:
        state = "error"
    return state

def accunlock(user_name, password):
    state = "error"
    #アドレス読み込み
    with open("add_dict.json",'r') as f:
        address_dict = json.load(f)
    if (user_name in address_dict) == True:
        unlock =  web3.personal.unlockAccount(address_dict[user_name],password,duration=hex(3600))
        state = user_name + " account unlock " + str(unlock)
    else:
        state = user_name + "You don't have address." 
    return state

def whatadd(me, men):
    ans = "error"
    with open("add_dict.json",'r') as f:
        address_dict = json.load(f)
    if( men in address_dict) == True:
        ans = me+"\n"+men+" 's address:\n" + address_dict[men]
    return ans

client = discord.Client()

@client.event
async def on_ready():
    print('bot logintest')
    print(client.user.name)
    print(client.user.id)
    print('-------------')

@client.event
async def on_message(message):
    #マジックナンバー
    if message.content.startswith("!manekinuko"):
        #メッセージ分割
        messagel_list = str(message.content).split(' ')
        #自分じゃないかの確認
        if client.user != message.author:
            if len(messagel_list)>1:
                #ウォレットの状態確認 ,! balance
                if (messagel_list[1] == balancecomm[1]) and (len(messagel_list) == len(balancecomm)):
                    say = balance(message.author.mention)
                    await client.send_message(message.channel,say)

                #ウォレット作成 ,! mkwallet
                elif (messagel_list[1] == mkwalletcomm[1]) and (len(messagel_list) == len(mkwalletcomm)):
                    print(messagel_list)
                    print(len(messagel_list))
                    #長さ確認
                    #パスワードがあってるかの確認
                    if messagel_list[2] == messagel_list[3]:
                        say = message.author.mention + " , make your wallet."
                        say = say + mkwallet(message.author.mention, messagel_list[2])
                        await client.send_message(message.channel,say)
                    else:
                        say = "error. " + messagel_list[2] + " != " + messagel_list[3] + " ."
                        await client.send_message(message.channel,say)

                #投げる .! tip @foo 123
                elif (messagel_list[1] == tippingcomm[1]) and (len(messagel_list) == len(tippingcomm)):
                    print(messagel_list)
                    print(message.author.mention)
                    print(messagel_list[3])
                    say = "tip " + message.author.mention + " to " + messagel_list[2] + " " + messagel_list[3] + " nuko\n"
                    say =say + tipping(message.author.mention,messagel_list[2],float(messagel_list[3]))
                    await client.send_message(message.channel,say)

                #アカウントアンロック ,! unlock password
                elif (messagel_list[1] == unlockcomm[1]) and (len(messagel_list) == len(unlockcomm)):
#                    say = message.author.mention + ", unlock. plz wait..."
#                    await client.send_message(message.channel,say)
                    say = accunlock(message.author.mention, messagel_list[2])
                    await client.send_message(message.channel,say)
                
                #keyストアの取得
                elif (messagel_list[1] == getkeycomm[1]) and (len(messagel_list) == len(getkeycomm)):
                    await client.send_file(message.channel,keystoredir+"/"+pkey(message.author.mention))

                #相手のアドレス表示
                elif (messagel_list[1] == whataddcomm[1]) and (len(messagel_list) == len(whataddcomm)):
                    say = whatadd(message.author.mention, messagel_list[2])
                    await client.send_message(message.channel,say)

                #help
                elif (messagel_list[1] == helpcomm[1]) and (len(messagel_list) == len(helpcomm)):
                    say = "=====================\n!manekinuko balance\nアカウントの状態を確認します．\n"
                    say = say + "============================\n!manekinuko mkwallet password1 password2\nアカウントを作成します．password1とpassword2は同じものを入力してください．\n"
                    say = say + "===========================\n!manekinuko tip @foobar value\n猫を投げます．valueはnukoの数値です\n"
                    say = say + "===========================\n!manekinuko unlock password\ntipする前にやってください．\n返答に時間がかかる場合があります．\n"
                    say = say + "===========================\n!manekinuko getkey\nkeystoreを受け取れます．\n"
                    say= say + "============================\n!manekinuko whatadd @foo\n相手のアドレスを表示します\n"
                    #await client.send_message(message.channel,say)
                    say = say + "\n開発中のためGOXする可能性があります．\n預けnukoは最小限におねがいします．\n"
                    say = say + "またmkwalletとunlockとgetkeyはbotとのDMで行うことをおすすめします．\n"
                    say = say + "getkeyは必ず行ってください\n"
                    say = say + "raspberry pi2で動いてますいじめないであげてください\n"
                    await client.send_message(message.channel,say)
                #error
                else:
                    say = "command error."
                    await client.send_message(message.channel,say)
            else:
                say = "command error. !manekinuko help"
                await client.send_message(message.channel,say)

client.run(bottoken,bool=False)
