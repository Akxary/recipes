from django.core.exceptions import ValidationError
from rest_framework import status

class MissingTokenException(ValidationError):
    def __init__(self):
        super().__init__("JWT token is missing", status.HTTP_401_UNAUTHORIZED, None)