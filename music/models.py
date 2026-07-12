from django.db import models


class Artist(models.Model):
    """
    歌手表：
    用来存储每一位歌手的基本信息。
    """

    kuwo_artist_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="酷我歌手ID"
    )

    artist_name = models.CharField(
        max_length=100,
        verbose_name="歌手名"
    )

    artist_image = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="歌手图片"
    )

    artist_intro = models.TextField(
        verbose_name="歌手简介"
    )

    artist_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="歌手原始URL"
    )

    birthday = models.CharField(
        max_length=100,
        default="暂无信息",
        verbose_name="生日"
    )

    country = models.CharField(
        max_length=100,
        default="暂无信息",
        verbose_name="国家/地区"
    )

    music_num = models.PositiveIntegerField(
        default=0,
        verbose_name="歌曲数量"
    )

    album_num = models.PositiveIntegerField(
        default=0,
        verbose_name="专辑数量"
    )

    class Meta:
        verbose_name = "歌手"
        verbose_name_plural = "歌手"
        ordering = ["artist_name"]

    def __str__(self):
        return self.artist_name


class Song(models.Model):
    """
    歌曲表：
    用来存储每一首歌曲的信息。
    """

    song_order = models.PositiveIntegerField(
        default=0,
        verbose_name="歌曲序号"
    )

    kuwo_song_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="酷我歌曲ID"
    )

    musicrid = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="MusicRID"
    )

    song_name = models.CharField(
        max_length=200,
        verbose_name="歌曲名"
    )

    artist = models.ForeignKey(
        Artist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="songs",
        verbose_name="关联歌手"
    )

    artist_name = models.CharField(
        max_length=200,
        verbose_name="歌手名"
    )

    keyword = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="搜索关键词"
    )

    album = models.CharField(
        max_length=200,
        default="无专辑归属",
        verbose_name="专辑"
    )

    duration = models.PositiveIntegerField(
        default=0,
        verbose_name="时长（秒）"
    )

    image_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="歌曲封面"
    )

    source_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="歌曲原始URL"
    )

    lyrics = models.TextField(
        verbose_name="歌词"
    )

    class Meta:
        verbose_name = "歌曲"
        verbose_name_plural = "歌曲"
        ordering = ["song_order"]

    def __str__(self):
        return f"{self.song_name} - {self.artist_name}"


class Comment(models.Model):
    """
    评论表：
    每一条评论属于某一首歌曲。
    """

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="所属歌曲"
    )

    nickname = models.CharField(
        max_length=50,
        default="匿名用户",
        verbose_name="昵称"
    )

    content = models.TextField(
        verbose_name="评论内容"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="评论时间"
    )

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.nickname} 对《{self.song.song_name}》的评论"