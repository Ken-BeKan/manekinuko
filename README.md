# manekinuko
NekoniumのDiscord用のTipボットです。  
Python3で書いています。

# 使い方
## 環境
1. gnekonium
1. discord.py 0.16.12
1. web3 3.16.4
1. Python 3.6
1. ubuntu 16.04

## gnekoniumの起動
gnekoniumを起動する
```bash
./gnekonium-linux-amd64 --rpc --rpcapi="db,eth,net,web3,personal,web3" --fast --cache=1024
```
## manekinukoの設定

## keystoreのディレクトリの設定
manekinukoにgnekoniumが作成するkeystoreのディレクトリを教えます。  
neko-tip.pyの7行目のkeystoredirにディレクトリを書いてください。
```python
#例
keystoredir = '/home/manekinuko/.nekonium/keystore
```

### tokenの設定
[discord developers](https://discordapp.com/developers)
でボットを作りtokenを取得します。
取得したtokenをnuko-tip.pyの8行目のbottokenに書いてください。
```python
#例
bottoken = '12345678910'
```
### manekinukoの起動
manekinukoを起動する。
```bash
python3 nuko-tip.py
```
