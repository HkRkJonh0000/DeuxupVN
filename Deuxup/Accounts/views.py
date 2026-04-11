from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import RegisterSerializer, UserSerializer

#Đăng ký tài khoản API
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Đăng nhập tài khoản API
class loginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerilizer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email = serializer.valicated_data["email"],
                password = serializer.valicated_data["password"]
                username = serializer.valicated_data["username"]
            )
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "token" : token.key,
                    "user" : UserSerializer(user).data,
                    "message" : "Đăng nhập thành công.",
                    "status" : status.HTTP_200_OK
                })
            else:
                return Response({
                    "message" : "Đăng nhập thất bại.",
                    "status" : status.HTTP_400_BAD_REQUEST,
                    "error": "Email hoặc mật khẩu không đúng.",
                })
        return Response("Lỗi xảy ra khi đăng nhập.", status=status.HTTP_401_UNAUTHORIZED)
    
#Lấy thông tin tài khoản API
class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data)
        if serialize.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)