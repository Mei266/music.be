from rest_framework.views import APIView
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from music.serializers import AlbumSerializers
from music.models import Album, Music
from rest_framework import status
from django.db.models import Count, Sum


class PopularAlbumViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: AlbumSerializers(many=True)})
    def get(self, request):
        try:
            album_listen_counts = Music.objects.values('album').annotate(total_listen=Sum('number_listens'))

            # Sắp xếp theo tổng số lượt nghe giảm dần và lấy 5 album đầu tiên
            top_5_albums = album_listen_counts.exclude(album=None).order_by('-total_listen')[:5]

            # Lấy danh sách các ID của 5 album có tổng số lượt nghe nhiều nhất
            top_5_album_ids = [item['album'] for item in top_5_albums]

            # Lấy thông tin chi tiết của các album từ các ID trên
            top_5_album_details = Album.objects.filter(pk__in=top_5_album_ids)

            serializer = AlbumSerializers(top_5_album_details, many=True)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )