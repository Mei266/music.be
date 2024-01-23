from rest_framework.views import APIView
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from music.models import Playlist, Music, User
from rest_framework import status
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from music.serializers import (
    PlaylistSerializers,
    PlaylistAddSerializers,
    MusicSerializers,
    PlaylistLimitMusicSerializers,
    PlaylistUpdateSerializers,
)


class PlayListViews(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: PlaylistSerializers(many=True)})
    def get(self, request, author_id):
        try:
            playlists = Playlist.objects.filter(author_id=author_id)
            # playlists.musics = playlists.musics[:5]
            serializer = PlaylistSerializers(playlists, many=True)
            data = serializer.data
            for playlist_data in data:
                playlist_data["music_list"] = playlist_data["music_list"][:5]
            return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PlayListCreateViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: PlaylistSerializers()})
    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
            index = Playlist.objects.count()
            playlist = Playlist.objects.create(
                title="My playlist " + str(index), author=user
            )
            serializer = PlaylistSerializers(playlist)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PlayListDetailViews(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(responses={200: PlaylistSerializers()})
    def get(self, request, id):
        try:
            playlist = Playlist.objects.get(id=id)
            serializer = PlaylistSerializers(playlist)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema()
    def delete(self, request, id):
        try:
            Playlist.objects.get(id=id).delete()
            return JsonResponse(
                {"message": "sucess delete" + str(id)},
                status=status.HTTP_200_OK,
                safe=False,
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=PlaylistUpdateSerializers, responses={200: PlaylistSerializers()}
    )
    def put(self, request, id):
        try:
            playlist = Playlist.objects.get(id=id)
            print(request.data["image"], "\n")
            print(request.data["title"], "\n")
            print(request.data["description"], "\n")
            if type(request.data["title"]) == str:
                print("x là một chuỗi")
            # print(1)
            # serializer = PlaylistUpdateSerializers(data=request.data)
            # print(2)
            # print(serializer.validated_data["image"], "\n")
            # print(3)
            if request.data["title"] != "null":
                playlist.title = request.data["title"]
            if request.data["image"]:
                playlist.image = request.data["image"]
            if request.data["description"] != "null":
                playlist.description = request.data["description"]
            playlist.save()
            serializer = PlaylistSerializers(playlist)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(responses={200: PlaylistSerializers()})
    def post(self, request):
        try:
            index = Playlist.objects.count()
            playlist = Playlist.objects.create(title="My playlist " + str(index))
            serializer = PlaylistSerializers(playlist)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# lấy playlist được tạo gần nhất
class PlayListMaxViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: PlaylistSerializers()})
    def get(self, request):
        try:
            playlist = Playlist.objects.order_by("id").first()
            serializer = PlaylistSerializers(playlist)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AddToPlayListViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        request_body=PlaylistAddSerializers, responses={200: PlaylistSerializers()}
    )
    def put(self, request, id):
        try:
            music_id = request.data["music_id"]
            music = Music.objects.get(id=music_id)
            playlist = Playlist.objects.get(id=id)
            playlist.musics.add(music)
            playlist.save()
            serializer = PlaylistSerializers(playlist)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RemoveToPlayListViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        request_body=PlaylistAddSerializers, responses={200: PlaylistSerializers()}
    )
    def put(self, request, id):
        try:
            music_id = request.data["music_id"]
            music = Music.objects.get(id=music_id)
            playlist = Playlist.objects.get(id=id)
            playlist.musics.remove(music)
            playlist.save()
            serializer = PlaylistSerializers(playlist)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PlaylistCountByAuthor(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema()
    def get(self, request, author_id):
        try:
            count = Playlist.objects.filter(author_id=author_id).count()
            return JsonResponse({"count": count}, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
