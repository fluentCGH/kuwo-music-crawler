import re
import json
import html as html_lib
import requests
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0",
    "Referer": "https://www.kuwo.cn/",
}

def extract_string_field(text,key):
    pattern = rf'{key}\s*:\s*"(.*?)"'
    match=re.search(pattern,text)
    if not match:
         return ""
    raw_value=match.group(1)
    try:
        value = json.loads('"' + raw_value + '"')
    except Exception:
        value = raw_value
    value = html_lib.unescape(value)

    return value
    

def extract_number_field(text,key):
    pattern=rf'{key}:\s*(\d+)'
    match = re.search(pattern, text)
    if not match:
        return 0

    return int(match.group(1))


def find_singer_script(html_text):
    soup=BeautifulSoup(html_text,"html.parser")
    scripts=soup.find_all("script")
    for script in scripts:
        script_text=script.get_text()
        if "singerInfo" in script_text:
            return script_text
    return ""

def fetch_artist_info(artist_id):
    artist_id = str(artist_id)
    artist_url = f"https://www.kuwo.cn/singer_detail/{artist_id}/info"

    response=requests.get(artist_url,headers=headers,timeout=10)
    response.raise_for_status()

    #print(response.headers.get("Content-Type"))
    #返回了text/html
    #print("状态码：",response.status_code)


    html_text=response.text
    target_script=find_singer_script(html_text)



    if target_script=="":
        print("没有找到 singerInfo，方法失败")
        return None
    else:
        section=target_script
        artist_intro=extract_string_field(section, "info")
        music_num=extract_number_field(section, "musicNum")
        birthday=extract_string_field(section, "birthday")
        country=extract_string_field(section, "country")
        if artist_intro=="" or str(music_num)=="0":
            return None
        if birthday=="":
            birthday="暂无信息"
        if country=="":
            country="暂无信息"
        artist={
            "artist_id": extract_number_field(section, "id"),
            "artist_name": extract_string_field(section, "name"),
            "artist_image": extract_string_field(section, "pic300"),
            "artist_intro": artist_intro,
            "artist_url": artist_url,
            "birthday": birthday,
            "country": country,
            "music_num": music_num,
            "album_num": extract_number_field(section, "albumNum"),
        }
    return artist

#artist=fetch_artist_info("336")
#print(artist)