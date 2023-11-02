from flask import Flask, jsonify, request
import io
import os
import json
import requests
import time
from urllib.parse import quote
import urllib
import math

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './env/api.json'

class calculate_kokuhaku:
    
    def calculate_negaposi(line_file_pick):
        
        # メタデータ社のAPIエンドポイント
        API_ENDPOINT = 'http://ap.mextractr.net/ma9/negaposi_analyzer'
        
        text = line_file_pick
               
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
        if (int(negaposi_late) == None):
            kokuhaku_late = 0
        elif (int(negaposi_late) <= 0):
            kokuhaku_late = 0
        else:
            kokuhaku_late = math.floor(negaposi_late * 49 + 1)
        return kokuhaku_late
    
    def kokuhaku_advice(kokuhaku_late):
        advice = ''      
        kokuhaku_late = int(kokuhaku_late)
        
        if kokuhaku_late <= 9: 
            advice = 'まだ親密な関係が築かれていないようです。相手とのコミュニケーションを増やし、共通の興味や趣味を見つけてみましょう。軽い会話や笑いを通じて相手をリラックスさせることが大切です。信頼関係を構築するのに時間をかけましょう。'
        elif kokuhaku_late >= 10 and kokuhaku_late <= 29:
            advice = '軽い友情や知り合いの関係ができています。この段階ではさらに深いコミュニケーションを取り、相手の興味や感情に注意を払いましょう。質問を通じて相手についてもっと知ることができます。相手の話に耳を傾け、共感を示すことが大切です。'
        elif kokuhaku_late >= 30 and kokuhaku_late <= 49:
            advice = '親密度が高まり、友情や信頼が築かれています。この段階では感情をより深く共有し、相手のサポートを提供できるようになります。関係をより強化するために、相手の喜びや悩みを共有し、協力関係を築いていきましょう。'
        elif kokuhaku_late >= 50 and kokuhaku_late <= 69:
            advice = 'かなり親密な関係が築かれています。相手を信頼し、支え合えるようになりました。これを維持するために、感謝の気持ちを表現しましょう。お互いのニーズや目標をサポートすることが大切です。共感と協力が関係を強化します。'
        elif kokuhaku_late >= 70 and kokuhaku_late <= 84:
            advice = '非常に親しい関係が築かれており、信頼が非常に高いです。この段階では、お互いの成長や幸福を促進し、時間を大切に過ごしましょう。信頼感を維持し、冷静にコミュニケーションを取りましょう。お互いのプライバシーと個人的な空間を尊重しましょう。'
        elif kokuhaku_late >= 85 and kokuhaku_late <= 99:
            advice = '非常に深い親密な関係が築かれており、お互いを完全に信頼しています。この段階では、お互いの幸福を支え、長期的な関係を維持しましょう。お互いの成功や挑戦に対して強力なサポートを提供し、感謝の意を表現しましょう。長期的な友情やパートナーシップを大切にし、新たな冒険を共に楽しんでください。'
        return advice
    
    def replay_advice(your_replay_speed, partner_replay_speed, partner_name):
       replay_speed_distance = abs(your_replay_speed - partner_replay_speed)
       
       replay_advice = ''
       
       replay_advice_one = 'あなたの返信速度の平均は{}分で、相手の返信速度の平均は{}分です。返信速度の平均の差は{}分あります。一般的に返信速度に差はない方が良いとされています。'.format(your_replay_speed, partner_replay_speed, replay_speed_distance)
       if (replay_speed_distance >= 1000):
           replay_advice_two = 'あなたと{}さんには返信速度に大きな差があります。あまり会話が続いていないのではないですか？心機一転、新しい話題を投げて話始めてはどうですか。'.format(partner_name)
       elif (your_replay_speed > partner_replay_speed):
           replay_advice_two = '{}さんははもっとあなたと会話したいと思っているかもしれません。返信速度をもう少し早くしてみてはどうですか。'.format(partner_name)
       else:
           replay_advice_two = '{}さんはもっとすっくりなペースで会話したいと思っているのかもしれません。返信速度をもう少し遅くしてみてはどうですか。'.format(partner_name)
           
       replay_advice = replay_advice_one + replay_advice_two
       
       
       
       return replay_advice