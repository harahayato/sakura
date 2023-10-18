# ライブラリのインポート
import requests
import math

f = open('myfile.txt', 'r', encoding='UTF-8')

text = f.read()
print(text)

f.close()

def point(self):
    
# APIに接続するための情報
    API_Endpoint = 'http://ap.mextractr.net/ma9/negaposi_analyzer'
    API_Key = "<API_KEY>"

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
        # json()メソッドを使うとレスポンスの内容を辞書または辞書のリストに変換して取得
    json_data = result.json()
    # negaposi要素(=ネガポジ度合いの数値)をaにいれる
    a = json_data['negaposi']

    # aが0以上だった場合には切り捨て+1、0未満だった場合には全てパラメータを0に変換
    if(a>=0):
        a = math.floor(a)+1
    else:
        a=0

    print(a)

    return a
