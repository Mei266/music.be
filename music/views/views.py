from rest_framework import serializers
from rest_framework import serializers, viewsets
from django.contrib import admin, auth
from music.models import User, Music
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from music.serializers import MusicSerializers


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = admin.models.LogEntry
        fields = "__all__"


class LogEntryViewSet(viewsets.ModelViewSet):
    queryset = admin.models.LogEntry.objects.all()
    serializer_class = LogEntrySerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class UserUpdateSerializer(serializers.Serializer):
    name = serializers.CharField()


class UsernameVerifiSerializer(serializers.Serializer):
    username = serializers.CharField()


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UsernameVerifiView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(request_body=UsernameVerifiSerializer)
    def post(self, request):
        try:
            username = request.data["username"]
            user = User.objects.filter(username=username)
            if user.exists():
                data = user.first()
                return JsonResponse({"acept": True, "userid": data.id, "username": data.username},status=status.HTTP_200_OK,)
            return JsonResponse(
                {"acept": False, "message": "Không tìm thấy tài khoản của bạn"},
                status=status.HTTP_200_OK,
            )
                
        except Exception:
            print("error")
            return JsonResponse(
                {"acept": False, "message": "Không tìm thấy tài khoản của bạn"},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserRegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]
            user = User.objects.create_user(
                username=username,
                password=password,
                is_staff=False,
                is_active=True,
            )
            return JsonResponse(
                {"acept": True, "data": user.username, "userid": user.id},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserUpdateView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        request_body=UserUpdateSerializer, responses={200: UserSerializer()}
    )
    def put(self, request, id):
        try:
            name = request.data["name"]
            user = User.objects.get(id=id)
            user.name = name
            user.save()
            serializer = UserSerializer(user)
            return JsonResponse(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserHeartView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: MusicSerializers(many=True)})
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = MusicSerializers(user.hearts, many=True)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserAddMusicSerializers(serializers.Serializer):
    music_id = serializers.IntegerField()


class UserAddMusicView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        request_body=UserAddMusicSerializers,
        responses={200: MusicSerializers(many=True)},
    )
    def post(self, request, id):
        try:
            music_id = request.data["music_id"]
            music = Music.objects.get(id=music_id)
            user = User.objects.get(id=id)
            user.hearts.add(music)
            user.save()
            serializer = MusicSerializers(user.hearts, many=True)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserRemoveMusicView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        request_body=UserAddMusicSerializers,
        responses={200: MusicSerializers(many=True)},
    )
    def post(self, request, id):
        try:
            music_id = request.data["music_id"]
            music = Music.objects.get(id=music_id)
            user = User.objects.get(id=id)
            user.hearts.remove(music)
            user.save()
            serializer = MusicSerializers(user.hearts, many=True)
            return JsonResponse(
                data=serializer.data, status=status.HTTP_200_OK, safe=False
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
