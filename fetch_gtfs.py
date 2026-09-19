import requests
from google.transit import gtfs_realtime_pb2
import csv
from datetime import datetime, timezone, timedelta
import os

# ⚠️ 注意：ここに本物のURL（http〜.pb）を必ず入れてください！ ⚠️
url = "URL（http〜.pb）"

# エラー防止：ファイルが存在しない場合は、まず空のファイルを作成する
if not os.path.exists('bus_history.csv'):
    with open('bus_history.csv', 'w', newline='', encoding='utf-8') as f:
        pass

# 日本時間の現在時刻を取得
JST = timezone(timedelta(hours=+9), 'JST')
now = datetime.now(JST)

try:
    # URLが仮のままなら実行しない
    if "ここ" in url:
        print("URLが変更されていません。")
    else:
        response = requests.get(url)
        if response.status_code == 200:
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            # 追記モードでCSVを開いて書き込む
            with open('bus_history.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                for entity in feed.entity:
                    if entity.HasField('vehicle'):
                        v = entity.vehicle
                        bus_number = v.vehicle.id if v.vehicle.id else "情報なし"
                        lat = v.position.latitude
                        lon = v.position.longitude
                        speed = round(v.position.speed * 3.6, 1) # km/hに変換
                        
                        writer.writerow([now.strftime('%Y-%m-%d %H:%M:%S'), bus_number, lat, lon, speed])
            print("データの保存に成功しました！")
        else:
            print(f"データの取得に失敗しました。ステータスコード: {response.status_code}")
except Exception as e:
    print(f"エラーが発生しました: {e}")
