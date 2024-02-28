from rest_framework.views import APIView
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from music.serializers import HeartSerializers, MusicSerializers
from music.models import Album, Music, Heart
from rest_framework import status
from django.db.models import Count, Sum


class HeartViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        request_body=HeartSerializers,
        responses={200: HeartSerializers(many=True)},
    )
    def post(self, request):
        try:
            serializer = HeartSerializers(data=request.data)
            if(serializer.is_valid()):
                serializer.save()
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HeartRemoveViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        request_body=HeartSerializers,
    )
    def post(self, request):
        try:
            print(request)
            heart = Heart.objects.filter(user=request.data['user'], music=request.data['music'])
            if heart :
                heart.delete()
                return JsonResponse(
                    data="Sucess", status=status.HTTP_200_OK, safe=False
                )
            return JsonResponse(
                    data="not found", status=status.HTTP_404_NOT_FOUND, safe=False
                )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HeartUserViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        responses={200: MusicSerializers(many=True)},
    )
    def get(self, request, id):
        try:
            hearts = Heart.objects.filter(user=id)
            print("musics: ", hearts)
            musics = [item.music for item in hearts]
            # res = Music.objects.filter(pk__in=music_ids)
            serializer = MusicSerializers(musics, many=True)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
