from .views import *
from .authentication import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    CustomTokenObtainPairView,
)
from .music import (
    MusicViews,
    MusicDetailViews,
    MusicRandomViews,
    MusicNextViews,
    MusicPreViews,
    MusicOtherInPlaylist,
    SearchMusic,
    HeartMusic,
    HeartListMusic,
    IncreaseListen,
    LatestMusicViews,
    TopMusicViews,
    PopularMusicViews
)

from .playlist import (
    PlayListViews,
    AddToPlayListViews,
    RemoveToPlayListViews,
    PlayListDetailViews,
    PlayListMaxViews,
    PlayListCreateViews,
    PlaylistCountByAuthor,
)

from .album import PopularAlbumViews
from .heart import HeartViews, HeartUserViews, HeartRemoveViews
from .search import SearchViews
