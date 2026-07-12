from time import perf_counter

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Artist, Comment, Song


def home(request):
    artist_count = Artist.objects.count()
    song_count = Song.objects.count()
    comment_count = Comment.objects.count()

    latest_songs = Song.objects.all()[:8]

    featured_keywords = [
        "周杰伦",
        "林俊杰",
        "陈奕迅",
        "张学友",
        "王力宏",
        "薛之谦",
        "邓紫棋",
        "蔡依林",
        "孙燕姿",
        "五月天",
        "Taylor Swift",
        "BIGBANG",
    ]

    popular_artists = []

    for keyword in featured_keywords:
        artist = Artist.objects.filter(
            artist_name__icontains=keyword
        ).first()

        if artist:
            popular_artists.append(artist)

    context = {
        "artist_count": artist_count,
        "song_count": song_count,
        "comment_count": comment_count,
        "latest_songs": latest_songs,
        "popular_artists": popular_artists,
    }

    return render(request, "music/home.html", context)


def song_list(request):
    query = request.GET.get("q", "").strip()[:20]

    songs = Song.objects.all()

    if query:
        songs = songs.filter(
            Q(song_name__icontains=query)
            | Q(artist_name__icontains=query)
            | Q(lyrics__icontains=query)
        )

    paginator = Paginator(songs, 20)
    raw_page = request.GET.get("page", "1").strip()

    try:
        page_value = float(raw_page)

        if page_value.is_integer() and page_value >= 1:
            page_number = int(page_value)
        else:
            page_number = 1

    except ValueError:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    context = { 
        "query": query,
        "page_obj": page_obj,
        "song_count": songs.count(),
    }

    return render(request, "music/song_list.html", context)


def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)

    comment_error = ""

    if request.method == "POST":
        nickname = request.POST.get("nickname", "").strip()
        content = request.POST.get("content", "").strip()

        if not nickname:
            nickname = "匿名用户"

        if content:
            Comment.objects.create(
                song=song,
                nickname=nickname,
                content=content,
            )

            return redirect("music:song_detail", pk=song.pk)

        comment_error = "评论内容不能为空。"

    related_songs = (
        Song.objects.filter(artist_name=song.artist_name)
        .exclude(pk=song.pk)[:6]
    )

    comments = song.comments.all()

    context = {
        "song": song,
        "related_songs": related_songs,
        "comments": comments,
        "comment_error": comment_error,
    }

    return render(request, "music/song_detail.html", context)


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    song_pk = comment.song.pk

    if request.method == "POST":
        comment.delete()

    return redirect("music:song_detail", pk=song_pk)


def artist_list(request):
    
    query = request.GET.get("q", "").strip()[:20]

    artists = Artist.objects.all()

    if query:
        artists = artists.filter(
            Q(artist_name__icontains=query)
            | Q(artist_intro__icontains=query)
        )

    paginator = Paginator(artists, 24)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "query": query,
        "page_obj": page_obj,
        "artist_count": artists.count(),
    }

    return render(request, "music/artist_list.html", context)


def artist_detail(request, pk):
    artist = get_object_or_404(Artist, pk=pk)

    songs = artist.songs.all()

    paginator = Paginator(songs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "artist": artist,
        "page_obj": page_obj,
        "song_count": songs.count(),
    }

    return render(request, "music/artist_detail.html", context)


def search(request):
    raw_query = request.GET.get("q", "").strip()

    query = raw_query[:20]
    query_truncated = len(raw_query) > 20

    search_type = request.GET.get("search_type", "song")

    if search_type not in ("song", "artist"):
        search_type = "song"

    if search_type == "artist":
        results = Artist.objects.none()
    else:
        results = Song.objects.none()

    search_time = None

    if query:
        start_time = perf_counter()

        if search_type == "artist":
            results = Artist.objects.filter(
                Q(artist_name__icontains=query)
                | Q(artist_intro__icontains=query)
            )
        else:
            results = Song.objects.filter(
                Q(song_name__icontains=query)
                | Q(artist_name__icontains=query)
                | Q(lyrics__icontains=query)
            )

        paginator = Paginator(results, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        page_obj.object_list = list(page_obj.object_list)

        result_count = paginator.count
        search_time = perf_counter() - start_time
    else:
        paginator = Paginator(results, 20)
        page_obj = paginator.get_page(1)
        result_count = 0

    context = {
        "query": query,
        "query_truncated": query_truncated,
        "search_type": search_type,
        "page_obj": page_obj,
        "result_count": result_count,
        "search_time": search_time,
    }

    return render(request, "music/search.html", context)