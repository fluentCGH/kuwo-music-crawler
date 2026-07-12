import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from music.models import Artist, Song, Comment


def safe_int(value, default=0):
    """
    把字符串或数字安全转换成 int。
    如果转换失败，就返回 default。
    """
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (ValueError, TypeError):
        return default


class Command(BaseCommand):
    help = "从 data 目录导入酷我音乐歌手和歌曲数据"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="导入前清空已有歌曲、歌手和评论数据"
        )

    def handle(self, *args, **options):
        base_dir = Path(settings.BASE_DIR)

        artists_path = base_dir / "data" / "artists_stage1.json"
        songs_path = base_dir / "data" / "songs_stage3_lyrics.json"

        if not artists_path.exists():
            self.stdout.write(self.style.ERROR(f"找不到歌手文件：{artists_path}"))
            return

        if not songs_path.exists():
            self.stdout.write(self.style.ERROR(f"找不到歌曲文件：{songs_path}"))
            return

        with open(artists_path, "r", encoding="utf-8") as f:
            artists_data = json.load(f)

        with open(songs_path, "r", encoding="utf-8") as f:
            songs_data = json.load(f)

        self.stdout.write(f"读取到歌手数据：{len(artists_data)} 条")
        self.stdout.write(f"读取到歌曲数据：{len(songs_data)} 条")

        with transaction.atomic():
            if options["clear"]:
                self.stdout.write("正在清空旧数据...")

                Comment.objects.all().delete()
                Song.objects.all().delete()
                Artist.objects.all().delete()

                self.stdout.write(self.style.WARNING("旧数据已清空"))

            artist_map = {}

            for item in artists_data:
                kuwo_artist_id = str(item.get("artist_id", "")).strip()

                if not kuwo_artist_id:
                    continue

                artist, created = Artist.objects.update_or_create(
                    kuwo_artist_id=kuwo_artist_id,
                    defaults={
                        "artist_name": item.get("artist_name", ""),
                        "artist_image": item.get("artist_image", ""),
                        "artist_intro": item.get("artist_intro", ""),
                        "artist_url": item.get("artist_url", ""),
                        "birthday": item.get("birthday", "暂无信息") or "暂无信息",
                        "country": item.get("country", "暂无信息") or "暂无信息",
                        "music_num": safe_int(item.get("music_num")),
                        "album_num": safe_int(item.get("album_num")),
                    }
                )

                artist_map[kuwo_artist_id] = artist

            self.stdout.write(self.style.SUCCESS(f"歌手导入完成：{Artist.objects.count()} 个"))

            missing_artist_count = 0

            for item in songs_data:
                kuwo_song_id = str(item.get("song_id", "")).strip()

                if not kuwo_song_id:
                    continue

                kuwo_artist_id = str(item.get("artist_id", "")).strip()
                artist = artist_map.get(kuwo_artist_id)

                if artist is None:
                    missing_artist_count += 1

                Song.objects.update_or_create(
                    kuwo_song_id=kuwo_song_id,
                    defaults={
                        "song_order": safe_int(item.get("song_order")),
                        "musicrid": item.get("musicrid", ""),
                        "song_name": item.get("song_name", ""),
                        "artist": artist,
                        "artist_name": item.get("artist_name", ""),
                        "keyword": item.get("keyword", ""),
                        "album": item.get("album", "无专辑归属") or "无专辑归属",
                        "duration": safe_int(item.get("duration")),
                        "image_url": item.get("image_url", ""),
                        "source_url": item.get("source_url", ""),
                        "lyrics": item.get("lyrics", ""),
                    }
                )

            self.stdout.write(self.style.SUCCESS(f"歌曲导入完成：{Song.objects.count()} 首"))

            if missing_artist_count > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f"有 {missing_artist_count} 首歌没有找到对应歌手详情，已保留歌曲但 artist 关联为空"
                    )
                )

        self.stdout.write(self.style.SUCCESS("全部数据导入完成！"))