from rest_framework_simplejwt.authentication import JWTAuthentication, Token
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.contrib.auth import get_user_model


Authors = get_user_model()

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token: Token):
        try:
            author_id = validated_token['author_id']
            user = Authors.objects.get(id=author_id)
            return user
        except Authors.DoesNotExist:
            raise AuthenticationFailed('Author not found')
        except KeyError:
            raise InvalidToken('Token contains no recognizable user identification')
