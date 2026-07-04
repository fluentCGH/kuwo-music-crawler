import json
import requests
import os
import time

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

input_path = BASE_DIR / "data" / "songs_stage2_favorite.json"
output_path = BASE_DIR / "data" / "songs_stage3_lyrics.json"

def load_songs():
    
    if output_path.exists():
        print("检测到已有 stage3 文件，从 stage3 继续读取")
        path = output_path
    else:
        print("未检测到 stage3 文件，从 stage2 开始读取")
        path = input_path

    with open(path,"r",encoding="utf-8") as f:
        songs=json.load(f)
    return songs

songs=load_songs()


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
    lyrics_text = "\n".join(lyrics)
    return lyrics_text

for i,song in enumerate(songs):
    if song.get("lyrics"):
        print("已有歌词，跳过：", song["song_name"])
        continue
    try:
        lyrics0=fetch_lyrics(song["song_id"])
    except Exception as e:
        print("歌词获取失败：", song["song_name"], song["song_id"], e)
        lyrics0 = ""
    songs[i]["lyrics"]=lyrics0

    if (i + 1) % 20 == 0:
        os.makedirs("../data",exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(songs, f, ensure_ascii=False, indent=2)
        print("阶段性保存：", i + 1)

    time.sleep(0.5)


with open(output_path,"w",encoding="utf-8") as f:
    json.dump(songs,f,ensure_ascii=False,indent=2)
print("已全部保存保存到 ../data/songs_stage3_lyrics.json")