from django.contrib.auth.models import AnonymousUser
from authentication.auth_api import send_verification_code, set_token, verify_code
from authors.models import Authors
from authors.serializers import ShortAuthorSerializer
from user_recipe.serializers import AuthorSerializer
from user_recipe.views import HttpMethods, logger
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from authentication.authentication import CustomJWTAuthentication


def get_author_by_email(request: Request) -> Authors:
    author, created_flg = Authors.objects.get_or_create(
        {"email": request.data.get("email")}
    )
    logger.info(
        "author with id %s was %s", author.id, "created" if created_flg else "got"
    )
    return author


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Authors.objects.all().order_by("email")

    @action(detail=False, methods=["post"], url_path="send-code")
    def send_code(self, request: Request) -> Response:
        email = request.data.get("email")
        try:
            send_verification_code(email)
            return Response(
                {"message": f"Verification code sent on {email}"},
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"message": f"Error while sending email on {email}: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"], url_path="verify-code")
    def verify_code(self, request: Request) -> Response:
        email = request.data.get("email")
        try:
            flg = verify_code(email, request.data.get("code", "-1"))
            if not flg:
                return Response(
                    {"message": "Verification code not accepted"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            return Response(set_token(email), status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(
                {"message": f"Error while verifing author {email}: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"], url_path="protected")
    @authentication_classes([CustomJWTAuthentication])
    @permission_classes([IsAuthenticated])
    def check_protectd(self, request: Request) -> Response:
        author: Authors | AnonymousUser = request.user
        if isinstance(author, AnonymousUser):
            return Response(
                {"message": "Error"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(
            {
                "message": f"This is a protected endpoint. Author {author.email} authorised"
            },
            status=status.HTTP_200_OK,
        )

    def get_serializer_class(self):
        if self.request.method == HttpMethods.POST.value:
            return ShortAuthorSerializer
        else:
            return AuthorSerializer
