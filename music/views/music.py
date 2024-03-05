from rest_framework.views import APIView
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from music.serializers import MusicSerializers, SearchMusicSerializers, ArtistSerializers, AlbumSerializers
from music.models import Music, Playlist, Heart, Artist, Album
from rest_framework import status
from django.db.models import Count


class MusicViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: MusicSerializers(many=True)})
    def get(self, request):
        try:
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

class IncreaseListen(APIView):
    authentication_classes = []
    permission_classes = []

    def put(self, request, id):
        try:
            music = Music.objects.get(id=id)
            music.number_listens += 1
            music.save()
            serializer = MusicSerializers(music)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LatestMusicViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: MusicSerializers(many=True)})
    def get(self, request):
        try:
            musics = Music.objects.order_by("-created_at")[:8]
            serializer = MusicSerializers(musics, many=True)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class TopMusicViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: MusicSerializers(many=True)})
    def get(self, request):
        try:
            musics = Music.objects.order_by("-number_listens")[:10]
            serializer = MusicSerializers(musics, many=True)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PopularMusicViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: MusicSerializers(many=True)})
    def get(self, request):
        try:
            # Thống kê số lượng người dùng yêu thích mỗi bài hát
            heart_counts = Heart.objects.values('music').annotate(user_count=Count('user'))

            # Sắp xếp theo số lượng người dùng giảm dần và lấy 5 bài hát đầu tiên
            top_5_music = heart_counts.order_by('-user_count')[:4]

            # Lấy danh sách các ID của 5 bài hát có số lượng người dùng yêu thích nhiều nhất
            top_5_music_ids = [item['music'] for item in top_5_music]

            # Lấy thông tin chi tiết của các bài hát từ các ID trên
            top_5_music_details = Music.objects.filter(pk__in=top_5_music_ids)
            serializer = MusicSerializers(top_5_music_details, many=True)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PopularMusicAlbumViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: MusicSerializers(many=True)})
    def get(self, request, id):
        try:
            artist = Artist.objects.get(pk=id)
            music_list = artist.artist_item.all()
            music_ids = []

            for item in music_list:
                music_ids.append({'id': item.id, 'popular': 0})
            # print(music_ids)
            for item in music_ids:
                popular = Heart.objects.filter(music=item['id']).values('music').annotate(user_count=Count('user'))
                if popular:
                    item['popular'] = popular[0]['user_count']
            sorted_elements = sorted(music_ids, key=lambda x: x['popular'], reverse=True)
            musics_rs = []
            for item in sorted_elements:
                # music = Music.objects.filter(pk=item['id'])
                musics_rs.append(item['id'])
            # Lấy các đối tượng Music theo id đã cho và sắp xếp theo thứ tự của các id
            music_objects = Music.objects.in_bulk(musics_rs)
            # print("music_objects: ", music_objects)

            # Tạo một list chứa các đối tượng Music theo thứ tự của các id đã cho
            sorted_music_list = [music_objects[id] for id in musics_rs if id in music_objects]
            # print("sorted_music_list: ", sorted_music_list)
            serializer = MusicSerializers(sorted_music_list, many=True)
            serializer_artist = ArtistSerializers(artist)
            return JsonResponse(
                {"artist": serializer_artist.data, "music_list": serializer.data}, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MusicAlbumViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: MusicSerializers(many=True)})
    def get(self, request, id):
        try:
            album = Album.objects.filter(pk=id)
            # musics = Music.objects.filter(album=id)
            # serializer = MusicSerializers(musics, many=True)
            serializer_album = AlbumSerializers(album, many=True)
            return JsonResponse(
                data=serializer_album.data, status=status.HTTP_200_OK, safe=False
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
