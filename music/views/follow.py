from rest_framework.views import APIView
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from music.serializers import FollowSerializers, ArtistSerializers
from music.models import Follow
from rest_framework import status


class FollowViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        request_body=FollowSerializers,
        responses={200: FollowSerializers(many=True)},
    )
    def post(self, request):
        try:
            follow = Follow.objects.filter(user=request.data['user'], artist=request.data['artist'])
            serializer = FollowSerializers(data=request.data)
            if serializer.is_valid() and not follow :
                serializer.save()
                return JsonResponse(
                    data=serializer.data, status=status.HTTP_201_CREATED, safe=False
                )
            return JsonResponse(
                {"message": "exits"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FollowRemoveViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        request_body=FollowSerializers,
    )
    def post(self, request):
        try:
            print(request)
            follow = Follow.objects.filter(user=request.data['user'], artist=request.data['artist'])
            if follow :
                follow.delete()
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

class FollowUserViews(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        responses={200: ArtistSerializers(many=True)},
    )
    def get(self, request, id):
        try:
            follows = Follow.objects.filter(user=id)
            musics = [item.artist for item in follows]
            serializer = ArtistSerializers(musics, many=True)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
