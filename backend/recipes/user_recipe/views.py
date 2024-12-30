from enum import Enum
import django.db.models as models
from rest_framework.response import Response
from rest_framework.request import Request
from user_recipe.models import Authors, Comments, Ingredients, Recipes, Stages
from rest_framework import viewsets, status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from user_recipe.serializers import (
    AuthorSerializer,
    CreateRecipeSerializer,
    ShortAuthorSerializer,
    CommentsSerializer,
    IngredientSerializer,
    RecipeSerializer,
    StageSerializer,
)

class HttpMethods(Enum):
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    GET = "GET"
    DELETE = "DELETE"
    
    @classmethod
    def values(cls) -> set[str]:
        return {m.value for m in cls if m.value != "GET"}


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Authors.objects.all().order_by("id")
    
    def get_serializer_class(self):
        if self.request.method == HttpMethods.POST.value:
            return ShortAuthorSerializer
        else:
            return AuthorSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all().order_by("id")
    
    def get_serializer_class(self):
        if self.request.method == HttpMethods.POST.value:
            return CreateRecipeSerializer
        else:
            return RecipeSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all().order_by("id")
    serializer_class = CommentsSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all().order_by("id")
    serializer_class = IngredientSerializer


class StageViewSet(viewsets.ModelViewSet):
    queryset = Stages.objects.all().order_by("order")
    serializer_class = StageSerializer

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "recipe_id": {"type": "integer", "example": 1, "description": "ID рецепта"},
                    "start_order": {"type": "integer", "example": 3, "description": "Начальный порядок"},
                },
                "required": ["recipe_id", "start_order"],
            }
        },
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
        description="Обновляет порядок стадий рецепта, начиная с указанного `start_order`.",
    )
    @action(detail=False, methods=["post"], url_path="reorder")
    def reorder_stages(self, request: Request) -> Response:
        """
        Обновление порядка стадий после указанного `n`.
        """
        recipe_id = request.data.get("recipe_id")
        start_order = request.data.get("start_order")

        if not recipe_id or start_order is None:
            return Response(
                {"error": "recipe_id and start_order are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        stages = Stages.objects.filter(recipe_id=recipe_id, order__gte=start_order)
        stages.update(order=models.F("order")+1)
        return Response({"message": "Stages reordered successfully."}, status=status.HTTP_200_OK)
    