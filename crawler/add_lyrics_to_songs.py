import json
import requests
import os
import time

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

input_path = BASE_DIR / "data" / "songs_stage2_favorite.json"
output_path = BASE_DIR / "data" / "songs_stage3_lyrics.json"
deleted_path = BASE_DIR / "data" / "deleted_lyrics_songs.json"      

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


valid_songs = []
deleted_lyrics_songs = []

for i, song in enumerate(songs):
    song["song_order"] = i + 1
    song_name = song.get("song_name", "")
    song_id = song.get("song_id", "")

    if song.get("lyrics"):
        print("已有歌词，跳过：", song_name)
        valid_songs.append(song)
    else:

        try:
            lyrics0 = fetch_lyrics(song_id)
        except Exception as e:
            print("歌词获取失败，删除：", song_name, song_id, e)

            deleted_lyrics_songs.append({
                "song_name": song_name,
                "song_id": song_id,
                "reason": "lyrics_request_failed"
            })

        else:
            if lyrics0.strip() == "":
                print("歌词为空，删除：", song_name, song_id)

                deleted_lyrics_songs.append({
                    "song_name": song_name,
                    "song_id": song_id,
                    "reason": "lyrics_empty"
                })

            else:
                song["lyrics"] = lyrics0
                valid_songs.append(song)

    
    if (i + 1) % 20 == 0:
        temp_songs = valid_songs + songs[i + 1:]

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(temp_songs, f, ensure_ascii=False, indent=2)

        with open(deleted_path, "w", encoding="utf-8") as f:
            json.dump(deleted_lyrics_songs, f, ensure_ascii=False, indent=2)

        print("阶段性保存：", i + 1)
        print("当前保留歌曲数：", len(valid_songs))
        print("当前删除无歌词歌曲数：", len(deleted_lyrics_songs))

    time.sleep(0.5)



with open(output_path, "w", encoding="utf-8") as f:
    json.dump(valid_songs, f, ensure_ascii=False, indent=2)

deleted_path = BASE_DIR / "data" / "deleted_lyrics_songs.json"
with open(deleted_path, "w", encoding="utf-8") as f:
    json.dump(deleted_lyrics_songs, f, ensure_ascii=False, indent=2)

print("已全部保存到：", output_path)
print("最终保留歌曲数：", len(valid_songs))
print("最终删除无歌词歌曲数：", len(deleted_lyrics_songs))

