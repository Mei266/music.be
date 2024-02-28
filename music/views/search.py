from rest_framework.views import APIView
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from music.serializers import AlbumSerializers, SearchMusicSerializers, MusicSerializers, ArtistSerializers
from music.models import Album, Music, Artist
from rest_framework import status
from django.db.models import Q


class SearchViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(request_body=SearchMusicSerializers,responses={200: AlbumSerializers(many=True)})
    def post(self, request):
        try:
            key_word = request.data['search_text']
            musics = Music.objects.filter(Q(name__icontains=key_word) | Q(lyric__icontains=key_word)).order_by('-number_listens')[:4]
            artists = Artist.objects.filter(name__icontains=key_word)
            albums = Album.objects.filter(title__icontains=key_word)
            musics_serializer = MusicSerializers(musics, many=True)
            artists_serializer = ArtistSerializers(artists, many=True)
            albums_serializer = AlbumSerializers(albums, many=True)

            return JsonResponse(
                data={
                    "musics": musics_serializer.data,
                    "artists": artists_serializer.data,
                    "albums": albums_serializer.data,
                }, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )