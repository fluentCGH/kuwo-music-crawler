from fetch_kuwo_artist import fetch_artist_info
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

input_path = BASE_DIR / "data" / "songs_stage3_lyrics.json"
output_path = BASE_DIR / "data" / "artists_stage1.json"

path=input_path
with open(path,"r",encoding="utf-8") as f:
        songs=json.load(f)

artists=[]
artist_id_check=set()
for song in songs:
    artist_id=str(song.get("artist_id",""))
    if artist_id=="" or artist_id=="0":
         continue
    elif artist_id in artist_id_check:
        continue
    else:
        try:
             artist=fetch_artist_info(artist_id)
        except Exception as e:
            print("歌手爬取失败：", artist_id, song.get("artist_id",""), e)
            continue
        if artist is not None:
            artists.append(artist)
            artist_id_check.add(artist_id)


with open(output_path,"w",encoding="utf-8") as f:
    json.dump(artists,f,ensure_ascii=False,indent=2)
print("已全部保存保存到",output_path)