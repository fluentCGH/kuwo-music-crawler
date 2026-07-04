# 酷我音乐爬虫项目记录

## Stage 1：单关键词多页搜索
- 文件：crawler/kuwo_search.py
- 输出：data/songs_stage1_jay.json
- 结果：周杰伦 20 页，约 400 条

## Stage 2：多关键词搜索与去重
- 文件：crawler/kuwo_search.py
- 输出：data/songs_stage2_favorite.json
- 关键词：周杰伦、林俊杰、陈奕迅、邓紫棋、孙燕姿
- 理论 300 条，去重后 299 条
- 重复歌曲：邓紫棋关键词下的《手心的蔷薇》，已在林俊杰关键词下出现