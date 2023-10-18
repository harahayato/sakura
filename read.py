# ライブラリのインポート
import requests
import math
import json

f = open('myfile.txt', 'r', encoding='UTF-8')

text = f.read()
print(text)

f.close()

    
# APIに接続するための情報
API_Endpoint = 'http://ap.mextractr.net/ma9/negaposi_analyzer'
#API_Key = 'api_key'

# リクエストヘッダを指定
headers = {
    "content-type":"application/json"
    }

# URLパラメータを指定
params = {
    'apikey':'',
    'out':'json',
    'text':text
    }

# request.getを使いレスポンスオブジェクトとしてresultをたてる
result=requests.get(API_Endpoint,headers=headers,params=params)
print(result)

# json()メソッドを使うとレスポンスの内容を辞書または辞書のリストに変換して取得
json_data = result.json()
print(json_data)

#json形式のデータをファイルで保存
filename = "result.json"
with open (filename, "w") as fp:
    json.dump(json_data, fp)

# negaposi要素(=ネガポジ度合いの数値)をaにいれる
a = json_data['negaposi']

print(a)

# aが0以上だった場合には切り捨て+1、0未満だった場合には全てパラメータを0に変換
if(a>=0):
    a = math.floor(a)+1
else:
    a=0
    
print(a)

