from typing import TypeVar
from rest_framework import serializers
from user_recipe.models import Authors, Recipes, Ingredients, Stages, Comments


class ExternalRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ["id", "recipe_name"]


class ShortAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ["id", "author_name"]


class AbstactFields:
    recipe: Recipes
    author: Authors


AbsFields = TypeVar("AbsFields", bound=AbstactFields)


class AbstractRecipeSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipes.objects.all())

    def to_representation(self, instance: AbsFields) -> dict:
        representation = super().to_representation(instance)
        recipe_instance = instance.recipe
        representation["recipe"] = ExternalRecipeSerializer(recipe_instance).data
        return representation


class AbstractAuthorSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Authors.objects.all())

    def to_representation(self, instance: AbsFields) -> dict:
        representation = super().to_representation(instance)
        author_instance = instance.author
        representation["author"] = ShortAuthorSerializer(author_instance).data
        return representation


class CommentsSerializer(AbstractRecipeSerializer):
    class Meta:
        model = Comments
        fields = ["id", "content", "recipe", "created_at", "updated_at"]


class AuthorSerializer(serializers.ModelSerializer):
    recipes = ExternalRecipeSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Authors
        fields = ["id", "author_name", "recipes", "comments", "created_at"]


class IngredientSerializer(AbstractRecipeSerializer):
    class Meta:
        model = Ingredients
        fields = ["id", "ingredient_name", "quantity", "unit", "recipe"]


class StageSerializer(AbstractRecipeSerializer):
    class Meta:
        model = Stages
        fields = ["id", "order", "description", "recipe"]


class CreateRecipeSerializer(AbstractAuthorSerializer):
    class Meta:
        model = Recipes
        fields = ["id", "recipe_name", "author"]


class RecipeSerializer(AbstractAuthorSerializer):
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Recipes
        fields = ["id", "recipe_name", "author", "comments", "created_at", "updated_at"]
