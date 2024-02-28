from django.urls import include, path
from rest_framework import routers
from music import views
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('data', basename='data')
# urlpatterns = router.urls

router = routers.DefaultRouter()
router.register(r"log-entry", views.LogEntryViewSet)
router.register(r"user", views.UserViewSet)

urlpatterns = [
    path("token/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", views.TokenVerifyView.as_view(), name="token_verify"),
    path(
        "login/username",
        views.UsernameVerifiView.as_view(),
        name="user name verifi",
    ),
    path("", include(router.urls)),
    # user
    path("user/register", views.UserRegisterView.as_view(), name="user register"),
    path("user/<int:id>/update", views.UserUpdateView.as_view(), name="user update"),
    # path("user/<int:id>/heart", views.UserHeartView.as_view(), name="user heart"),
    path(
        "user/<int:id>/music/add", views.UserAddMusicView.as_view(), name="user heart"
    ),
    path(
        "user/<int:id>/music/remove",
        views.UserRemoveMusicView.as_view(),
        name="user heart",
    ),
    # music
    path("music", views.MusicViews.as_view(), name="get all music"),
    path("music/latest", views.LatestMusicViews.as_view(), name="get 8 lastest music"),
    path("music/<int:id>/increase", views.IncreaseListen.as_view(), name="increase listen"),
    path("music/<int:id>", views.MusicDetailViews.as_view(), name="get music"),
    path(
        "music/random/<int:id>",
        views.MusicRandomViews.as_view(),
        name="get random music",
    ),
    path("music/next/<int:id>", views.MusicNextViews.as_view(), name="get next music"),
    path("music/prev/<int:id>", views.MusicPreViews.as_view(), name="get prev music"),
    path("music/<int:id>/heart", views.HeartMusic.as_view(), name="heart music"),
    path("music/heart", views.HeartListMusic.as_view(), name="heart list music"),
    # playlist
    path(
        "playlist/author/<int:author_id>",
        views.PlayListViews.as_view(),
        name="get post playlist",
    ),
    path(
        "user/<int:id>/playlist",
        views.PlayListCreateViews.as_view(),
        name="get post playlist",
    ),
    path(
        "playlist/<int:id>",
        views.PlayListDetailViews.as_view(),
        name="get playlist detail",
    ),
    path(
        "playlist/<int:id>/add",
        views.AddToPlayListViews.as_view(),
        name="add music to playlist",
    ),
    path(
        "playlist/<int:id>/remove",
        views.RemoveToPlayListViews.as_view(),
        name="add music to playlist",
    ),
    path(
        "playlist/max",
        views.PlayListMaxViews.as_view(),
        name="get playlist",
    ),
    path(
        "playlist/<int:id>/suggestion",
        views.MusicOtherInPlaylist.as_view(),
        name="get 5 music",
    ),
    path(
        "playlist/<int:id>/search",
        views.SearchMusic.as_view(),
        name="search music",
    ),
    path(
        "playlist/count/<int:author_id>",
        views.PlaylistCountByAuthor.as_view(),
        name="count by author",
    ),
    # home
    path(
        "home/latest",
        views.LatestMusicViews.as_view(),
        name="get 8 music lastest",
    ),
    path(
        "home/popular_music",
        views.PopularMusicViews.as_view(),
        name="get 4 popular music",
    ),
    path(
        "home/popular_album",
        views.PopularAlbumViews.as_view(),
        name="get 4 album popular",
    ),
    path(
        "home/top",
        views.TopMusicViews.as_view(),
        name="get top 10 mmusic",
    ),
    # Heart
    path(
        "heart",
        views.HeartViews.as_view(),
        name="heart",
    ),
    path(
        "heart",
        views.HeartViews.as_view(),
        name="heart",
    ),
    path(
        "heart/delete",
        views.HeartRemoveViews.as_view(),
        name="user heart",
    ),
    # search
    path(
        "search",
        views.SearchViews.as_view(),
        name="search music, artist, album",
    ),
]
