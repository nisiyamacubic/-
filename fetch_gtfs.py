import requests
from google.transit import gtfs_realtime_pb2
import csv
from datetime import datetime, timezone, timedelta

# 日本時間の現在時刻を取得
JST = timezone(timedelta(hours=+9), 'JST')
now = datetime.now(JST)

# URLを本物のGTFS Realtime(VehiclePositions)のものに変更してください
url = "ここに_カリー観光バスの_VehiclePositions_URL_を入れます"

try:
    response = requests.get(url)
    if response.status_code == 200:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        
        # 追記モード('a')でCSVファイルを開く
        with open('bus_history.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            for entity in feed.entity:
                if entity.HasField('vehicle'):
                    v = entity.vehicle
                    bus_number = v.vehicle.label if v.vehicle.label else "情報なし"
                    lat = v.position.latitude
                    lon = v.position.longitude
                    speed = round(v.position.speed * 3.6, 1) # km/hに変換
                    
                    # 日時, 車両番号, 緯度, 経度, 速度 の順番でCSVに書き込む
                    writer.writerow([now.strftime('%Y-%m-%d %H:%M:%S'), bus_number, lat, lon, speed])
                    
except Exception as e:
    print(f"エラー: {e}")
