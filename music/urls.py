from django.urls import path

from . import views


app_name = "music"


urlpatterns = [
    path("", views.home, name="home"),

    path("songs/", views.song_list, name="song_list"),
    path("songs/<int:pk>/", views.song_detail, name="song_detail"),

    path(
        "comments/<int:comment_id>/delete/",
        views.delete_comment,
        name="delete_comment",
    ),

    path("artists/", views.artist_list, name="artist_list"),
    path("artists/<int:pk>/", views.artist_detail, name="artist_detail"),

    path("search/", views.search, name="search"),
]