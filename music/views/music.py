from rest_framework.views import APIView
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from music.serializers import MusicSerializers, SearchMusicSerializers
from music.models import Music, Playlist
from rest_framework import status
from mysite import settings


class MusicViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: MusicSerializers(many=True)})
    def get(self, request):
        try:
            print(settings.SECRET_KEY)
            musics = Music.objects.all().order_by("created_at")
            serializer = MusicSerializers(musics, many=True)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(responses={200: MusicSerializers()})
    def update(self, request, id):
        try:
            music = Music.objects.get(id=id)
            serializer = MusicSerializers(music)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MusicDetailViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: MusicSerializers()})
    def get(self, request, id):
        try:
            music = Music.objects.all().get(id=id)
            serializer = MusicSerializers(music)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MusicRandomViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: MusicSerializers()})
    def get(self, request, id):
        try:
            # total = Music.objects.count()
            # random_index = random.randint(0, total - 1)
            # music = Music.objects.get(id=random_index)
            music = Music.objects.exclude(id=id).order_by("?").first()
            serializer = MusicSerializers(music)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MusicNextViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: MusicSerializers()})
    def get(self, request, id):
        try:
            # total = Music.objects.count()
            # random_index = random.randint(0, total - 1)
            # music = Music.objects.get(id=random_index)
            max_id_record = Music.objects.order_by("-id").first()
            music = None
            if max_id_record.id == id:
                music = Music.objects.order_by("id").first()
            else:
                music = Music.objects.filter(id__gt=id).first()
            serializer = MusicSerializers(music)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MusicPreViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: MusicSerializers()})
    def get(self, request, id):
        try:
            # total = Music.objects.count()
            # random_index = random.randint(0, total - 1)
            # music = Music.objects.get(id=random_index)
            min_record = Music.objects.order_by("id").first()
            music = None
            if min_record.id == id:
                music = Music.objects.order_by("-id").first()
            else:
                music = Music.objects.filter(id__lt=id).order_by("-id").first()
            serializer = MusicSerializers(music)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MusicOtherInPlaylist(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: MusicSerializers(many=True)})
    def get(self, request, id):
        try:
            playlist = Playlist.objects.get(id=id)
            s = MusicSerializers(playlist.musics, many=True)
            ids = []
            for item in s.data:
                ids.append(item["id"])
            musics = Music.objects.exclude(id__in=ids).order_by("created_at")
            serializer = MusicSerializers(musics, many=True)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SearchMusic(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        request_body=SearchMusicSerializers,
        responses={200: MusicSerializers(many=True)},
    )
    def post(self, request, id):
        try:
            playlist = Playlist.objects.get(id=id)
            s = MusicSerializers(playlist.musics, many=True)
            ids = []
            for item in s.data:
                ids.append(item["id"])
            search_text = request.data["search_text"]
            musics = (
                Music.objects.exclude(id__in=ids)
                .filter(name__icontains=search_text)
                .order_by("created_at")
            )
            serializer = MusicSerializers(musics, many=True)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HeartMusic(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        responses={200: MusicSerializers()},
    )
    def put(self, request, id):
        try:
            music = Music.objects.get(id=id)
            if music.heart:
                music.heart = False
            else:
                music.heart = True
            music.save()
            serializer = MusicSerializers(music)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HeartListMusic(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        responses={200: MusicSerializers(many=True)},
    )
    def get(self, request):
        try:
            music = Music.objects.filter(heart=True)
            serializer = MusicSerializers(music, many=True)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
