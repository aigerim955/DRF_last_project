# from django.contrib.auth import get_user_model, authenticate
# from rest_framework import serializers
#
# from .utils import send_activation_mail
#
# User = get_user_model()
#
#
# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(min_length=6, required=True)
#     password_confirm = serializers.CharField(min_length=6, required=True)
#
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'password_confirm',
#                   'name', 'last_name')
#
#     def validate_email(self, email):
#         if User.objects.filter(email=email).exists():
#             raise serializers.ValidationError('Такой пользователь уже зарегистрирован')
#         return email
#
#     def validate(self, attrs):
#         password = attrs.get('password')
#         password_confirm = attrs.pop('password_confirm')
#         if password != password_confirm:
#             raise serializers.ValidationError('Пароли не совпадают')
#         return attrs
#
#     def save(self,**kwargs):
#         email = self.validated_data.get('email')
#         password = self.validated_data.get('password')
#         user = User.objects.create_user(
#             email, password
#         )
#         return user
#
#
#
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(style={'input_type': 'password'})
#
#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#
#         if email and password:
#             user = authenticate(username=email, password=password,
#                                 request=self.context.get('request'))
#             if not user:
#                 raise serializers.ValidationError('Неверно указан email или пароль', code='authorization')
#         else:
#             raise serializers.ValidationError('Email и пароль обязательны')
#         attrs['user'] = user
#         return attrs

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6,required=True)
    password_confirmation = serializers.CharField(min_length=6,required=True)


    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'password', 'password_confirmation')


    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('User with this username alredy exists')
        return value


    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email already exists')
        return value


    def validate(self,attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Paroli ne sovpadaut')
        return attrs


    def save(self,**kwargs):
        username = self.validated_data.get('username')
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        name = self.validated_data.get('username')
        user = User.objects.create_user(
            username,email,password,name=name
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


    def validate(self,attrs):
        username = attrs.get('username')
        password = attrs.get('password')


        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,password=password
            )

            if not user:
                raise serializers.ValidationError('Access denied.',code='authorization')


        else:
            raise serializers.ValidationError(
                'need to enter "username" and "password".'
            )
        attrs['user'] = user
        return attrs