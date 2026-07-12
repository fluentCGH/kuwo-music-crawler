from django.contrib import admin
from .models import Artist, Song, Comment


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "artist_name",
        "kuwo_artist_id",
        "country",
        "birthday",
        "music_num",
        "album_num",
    )
    search_fields = (
        "artist_name",
        "kuwo_artist_id",
        "country",
    )
    list_filter = (
        "country",
    )


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "song_order",
        "song_name",
        "artist_name",
        "album",
        "duration",
        "kuwo_song_id",
    )
    search_fields = (
        "song_name",
        "artist_name",
        "album",
        "lyrics",
        "kuwo_song_id",
    )
    list_filter = (
        "artist_name",
        "album",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "song",
        "nickname",
        "created_at",
    )
    search_fields = (
        "nickname",
        "content",
        "song__song_name",
    )
    list_filter = (
        "created_at",
    )