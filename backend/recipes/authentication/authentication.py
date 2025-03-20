from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

from redis_api.redis_api import RedisClient


Authors = get_user_model()


class CustomJWTAuthentication(JWTAuthentication):

    def authenticate(self, request: Request):
        # Получаем токен из заголовка
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        raw_token = self.get_raw_token()
        if not raw_token:
            return None

        try:
            # Декодируем токен, чтобы извлечь email
            validated_token = self.get_validated_token(raw_token)
            email = validated_token["email"]  # Предполагаем, что email есть в токене
        except Exception as e:
            raise AuthenticationFailed("Invalid token")
        redis_client = RedisClient(email)
        # Получаем токен из Redis по email
        if not redis_client.check_current_author_jwt(raw_token.decode()):
            raise AuthenticationFailed("Redis token mismatched")

        # Получаем автора по email
        try:
            author = Authors.objects.get(email=email)
        except Authors.DoesNotExist:
            raise AuthenticationFailed("Author not found")

        return (author, raw_token)
