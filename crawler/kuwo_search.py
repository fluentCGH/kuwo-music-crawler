#https://kuwo.cn/search/searchMusicBykeyWord?vipver=1&client=kt&ft=music&cluster=0&strategy=2012&encoding=utf8&rformat=json&mobi=1&issubtitle=1&show_copyright_off=1&pn=0&rn=20&all=%E5%91%A8%E6%9D%B0%E4%BC%A6

import requests
import json
import time
import os
url="https://kuwo.cn/search/searchMusicBykeyWord"

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0",
    "Referer":"https://kuwo.cn"
}

keywords=["周杰伦","林俊杰","陈奕迅","邓紫棋","孙燕姿"]
songs=[]
seen_song_ids=set()
duplicate_songs=[]

for keyword in keywords:
    for page in range(3):
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
            "pn": str(page),
            "rn": "20",
            "all": keyword,
        }
        response=requests.get(url,params=params,headers=headers,timeout=10)

        response.raise_for_status()
        
        data=response.json()

        items = data.get("abslist", [])

        print("正在爬",keyword,"的第", page, "页，本页数量：", len(items))

        for item in items:
            song_id=item.get("DC_TARGETID","")
            if not song_id:
                continue
            if song_id in seen_song_ids:
                duplicate_songs.append({
                    "keyword": keyword,
                    "song_name": item.get("SONGNAME") or item.get("NAME", ""),
                    "artist_name": item.get("ARTIST", ""),
                    "song_id": song_id,
                })
                continue

            seen_song_ids.add(song_id)
            song = {
                "song_order":len(songs) + 1,
                "song_name": item.get("SONGNAME") or item.get("NAME", ""),
                "keyword":keyword,
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
        time.sleep(0.01)

print("爬取完成，歌曲数量：", len(songs))

os.makedirs("../data", exist_ok=True)

with open("../data/songs_stage2_favorite.json","w",encoding="utf-8") as f:
    json.dump(songs,f,ensure_ascii=False,indent=2)

print("已保存到 ../data/songs_stage2_favorite.json")

print("重复跳过数量：", len(duplicate_songs))
keyword_count = {}

for song in songs:
    keyword = song["keyword"]
    keyword_count[keyword] = keyword_count.get(keyword, 0) + 1

print("每个关键词实际保存数量：")
for keyword, count in keyword_count.items():
    print(keyword, count)

for song in duplicate_songs:
    print(song)