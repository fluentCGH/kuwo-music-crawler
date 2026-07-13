import json
import requests

url="https://kuwo.cn/search/searchMusicBykeyWord"

params={
    "vipver": "1",
    "client": "kt",
    "ft": "music",
    "cluster": "0",
    "strategy": "2012",
    "encoding": "utf8",
    "rformat": "json",
    "mobi": "1",
    "issubtitle": "1",
    "show_copyright_off": "1",
    "pn": "1",
    "rn": "20",
    "all": "周杰伦",
}

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0",
    "Referer":"https://kuwo.cn"
}

response=requests.get(url,params=params,headers=headers,timeout=10)

print("status_code:",response.status_code)
print("Content-Type:",response.headers.get("Content-Type"))
print("final_url:", response.url)
print("text_start:", response.text[:300])

response.raise_for_status()

data=response.json()

print("TOTAL:", data.get("TOTAL"))
print("PN:", data.get("PN"))
print("RN:", data.get("RN"))
print("本页歌曲数量:", len(data.get("abslist", [])))

songs = []

for item in data.get("abslist", []):
    song_id = item.get("DC_TARGETID", "")

    song = {
        "song_name": item.get("SONGNAME") or item.get("NAME", ""),
        "artist_name": item.get("ARTIST", ""),
        "artist_id": item.get("ARTISTID", ""),
        "song_id": song_id,
        "musicrid": item.get("MUSICRID", ""),
        "album": item.get("ALBUM", ""),
        "duration": item.get("DURATION", ""),
        "image_url": item.get("hts_MVPIC", ""),
        "source_url": f"https://www.kuwo.cn/play_detail/{song_id}",
    }

    songs.append(song)

print("\n前 5 条整理结果：")
for i, song in enumerate(songs[:5], start=1):
    print(f"\n第 {i} 首")
    print("歌曲名：", song["song_name"])
    print("歌手名：", song["artist_name"])
    print("歌手ID：", song["artist_id"])
    print("歌曲ID：", song["song_id"])
    print("MUSICRID：", song["musicrid"])
    print("专辑：", song["album"])
    print("时长：", song["duration"])
    print("图片：", song["image_url"])
    print("原始URL：", song["source_url"])

    import os
    os.makedirs("../data",exist_ok=True)

    with open("../data/songs_sample.json","w",encoding="utf-8") as f:
        json.dump(songs,f,ensure_ascii=False,indent=2)

    print("\n已保存到 ../data/songs_sample.json")