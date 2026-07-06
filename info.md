# 数据提取链路

### 1. 歌手列表页 Playwright 抓名字
##### #file:=="fetch_kuwo_artist_seeds_playwright.py"==
##### #input:None
##### #output:"artist_names_stage1.json"

    
### 2.用歌手名作为 keyword 搜歌曲
##### #file:=="kuwo_search.py"==
##### #input:"artist_names_stage1.json"
##### #output:"songs_stage2_favorite.json"    
    
### 3.歌曲信息中补充歌词
##### #file:=="add_lyrics_to_songs.py"==
##### #input:"songs_stage2_favorite.json"
##### #output:"songs_stage3_lyrics.json"
    
### 4.从歌曲 artist_id 反查歌手详情
##### #asist:=="fetch_kuwo_artist.py"==
##### #file:=="crawl_kuwo_artists.py"==
##### #input:"songs_stage3_lyrics.json"
##### #output:"artists_stage1.json"