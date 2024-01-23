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
