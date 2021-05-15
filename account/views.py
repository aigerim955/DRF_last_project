from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer
from .utils import send_activation_mail


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_activation_mail(user)
            return Response('Пользователь успешно зарегистрирован. Пожалуйста, проверьте почту для активации.',
                            status.HTTP_201_CREATED)


class ActivationView(APIView):
    def get(self, request, activation_code):
        # activation_code = request.query_params.get('u')
        User = get_user_model()
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Аккаунт успешно активирован', status=200)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        #from rest_framework.authtoken.models import Token
        Token.objects.filter(user=user).delete()
        return Response('Вы успешно вышли', status=200)

