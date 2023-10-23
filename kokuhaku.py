from flask import Flask, jsonify, request
import io
import os
import json
import requests
import time
from urllib.parse import quote
import urllib

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './env/api.json'

class calculate_kokuhaku:
    
    def change_line_file(line_file):
        line_file_after = line_file     
        
        #LINEファイルの形式を変換する
        
        
        return line_file_after
    
    def calculate_negaposi(line_file_pick):
        
        # メタデータ社のAPIエンドポイント
        API_ENDPOINT = 'http://ap.mextractr.net/ma9/negaposi_analyzer'
        
        text = str(line_file_pick)
               
        # リクエストヘッダを指定
        headers = {
            "content-type":"application/json"
            }
        
        params = {
            'apikey':'',
            'out':'json',
            'text':text
            } 
        
        # request.getを使いレスポンスオブジェクトとしてresultをたてる
        result = requests.get(API_ENDPOINT,headers=headers,params=params)
        
        json_data = result.json()
                  
        # negaposi要素(=ネガポジ度合いの数値)をaにいれる
        negaposi_late = json_data['negaposi']

        # 結果を表示するテンプレートにリダイレクト
        return negaposi_late
    
    def calculate_kokuhaku_late(negaposi_late):
        if (negaposi_late <= 0):
            kokuhaku_late = 0
        else:
            kokuhaku_late = round(negaposi_late * 33.3)
        return kokuhaku_late