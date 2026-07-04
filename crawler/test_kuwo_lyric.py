#https://www.kuwo.cn/openapi/v1/www/lyric/getlyric?musicId=228908&httpsStatus=1&reqId=8332d0d0-7784-11f1-80a0-d563fd188820&plat=web_www&from=

import json
import requests
import os

url="https://www.kuwo.cn/openapi/v1/www/lyric/getlyric"
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0",
    "Referer":"https://kuwo.cn"
}
params={
    "musicId":"228908",
    "httpsStatus":"1",
    "reqId":"8332d0d0-7784-11f1-80a0-d563fd188820&",
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

os.makedirs("../data",exist_ok=True)
with open("../data/lyrics_sample.json","w",encoding="utf-8") as f:
        json.dump(lyrics,f,ensure_ascii=False,indent=2)