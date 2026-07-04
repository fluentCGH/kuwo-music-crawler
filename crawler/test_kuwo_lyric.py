#https://www.kuwo.cn/openapi/v1/www/lyric/getlyric?musicId=228908&httpsStatus=1&reqId=8332d0d0-7784-11f1-80a0-d563fd188820&plat=web_www&from=

import json
import requests
import os

url="https://www.kuwo.cn/openapi/v1/www/lyric/getlyric"
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0",
    "Referer":"https://kuwo.cn"
}
def fetch_lyrics(song_id):
    params={
        "musicId":str(song_id),
        "httpsStatus":"1",
        "plat":"web_www",
        "from":"",
    }


    response=requests.get(url,headers=headers,params=params,timeout=10)

    response.raise_for_status()

    data=response.json()

    lyrics=[]
    lyric_list = data.get("data", {}).get("lrclist", [])
    for line in lyric_list:
        lyrics.append(line.get("lineLyric",""))
    return lyrics
lyrics = fetch_lyrics("228908")

print("歌词预览：")
print(lyrics[:500])

os.makedirs("../data", exist_ok=True)

with open("../data/lyrics_sample.json", "w", encoding="utf-8") as f:
    json.dump(lyrics, f, ensure_ascii=False, indent=2)

print("已保存到 ../data/lyrics_sample.json")