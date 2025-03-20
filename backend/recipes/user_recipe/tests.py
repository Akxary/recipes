import logging
from typing import TypeVar
from rest_framework import status
from django.db.models import Model
from authors.models import Authors
from authors.tests import MockAuthor
from user_recipe.models import Ingredients, Recipes, Stages

logger = logging.getLogger(__name__)




class MockRecipe(MockAuthor):
    def get_mock_recipe(
        self,
        author: Authors | None = None,
        sub_data: dict | None = None,
    ) -> Recipes:
        if author is None:
            author = self.get_mock_author()
        data = {"recipe_name": "Pizza", "author": author}
        if sub_data is not None:
            data.update(sub_data)
        return Recipes.objects.create(**data)


class MockIngredients(MockRecipe):
    def get_mock_ingredient(
        self,
        recipe: Recipes | None = None,
        sub_data: dict | None = None,
    ) -> Ingredients:
        if recipe is None:
            recipe = self.get_mock_recipe()
        data = {
            "ingredient_name": "Egg",
            "quantity": 1,
            "unit": Ingredients.Units.COUNT.value,
            "recipe": recipe,
        }
        if sub_data is not None:
            data.update(sub_data)
        return Ingredients.objects.create(**data)


class MockStages(MockRecipe):
    def get_mock_stage(
        self,
        recipe: Recipes | None = None,
        sub_data: dict | None = None,
    ) -> Stages:
        if recipe is None:
            recipe = self.get_mock_recipe()
        data = {
            "order": 1,
            "description": "Fizz buzz",
            "recipe": recipe,
        }
        if sub_data is not None:
            data.update(sub_data)
        return Stages.objects.create(**data)


class RecipeAPITest(MockRecipe):
    base_url = "/api/recipes/"

    def test_create_recipe(self) -> None:
        """Тестируемм создание рецепта"""
        author = self.get_mock_author()
        data = {"recipe_name": "Pie", "author": author.id}
        response = self.client.post(self.base_url, data)
        data["author"] = author.author_name
        self.check_single_response(response, status.HTTP_201_CREATED, data)

    def test_update_recipe(self) -> None:
        """Тестируем обновление рецепта"""
        recipe = self.get_mock_recipe()
        data = {"recipe_name": "Buzz"}
        response = self.client.patch(self.base_url + f"{recipe.id}/", data)
        self.check_single_response(response, status.HTTP_200_OK, data)

    def test_list_recipes(self) -> None:
        """Тестируем получения списка рецептов"""
        author = self.get_mock_author()
        recipe_list = [
            {"recipe_name": "Fizz", "author": author},
            {"recipe_name": "Buzz", "author": author},
        ]
        Recipes.objects.bulk_create([Recipes(**item) for item in recipe_list])
        response = self.client.get(self.base_url)
        self.check_list_response(response, 2)

    def test_delete_recipe(self) -> None:
        """Тестируем удаление рецепта"""
        recipe = self.get_mock_recipe()
        response = self.client.delete(self.base_url + f"{recipe.id}/")
        self.check_delete_response(response, Recipes)


class IngredientAPITest(MockIngredients):
    base_url = "/api/ingredients/"

    def test_create_ingredient(self) -> None:
        """Создание ингредиента"""
        recipe = self.get_mock_recipe()
        data = {
            "ingredient_name": "fizz",
            "quantity": 10,
            "unit": Ingredients.Units.GRAMM.value,
            "recipe": recipe.id,
        }
        response = self.client.post(self.base_url, data)
        data["recipe"] = {"id": recipe.id, "recipe_name": recipe.recipe_name}
        self.check_single_response(response, status.HTTP_201_CREATED, data)

    def test_update_ingredient(self) -> None:
        """Обновление ингредиента"""
        ingredient = self.get_mock_ingredient()
        data = {"quantity": ingredient.quantity + 1}
        response = self.client.patch(f"{self.base_url}{ingredient.id}/", data)
        self.check_single_response(response, status.HTTP_200_OK, data)

    def test_list_ingredients(self) -> None:
        """Получение списка ингредиентов"""
        recipe = self.get_mock_recipe()
        data_list = [
            self.get_mock_ingredient(recipe),
            self.get_mock_ingredient(recipe, {"ingredient_name": "fizzbuzz"}),
        ]
        response = self.client.get(self.base_url)
        self.check_list_response(response, 2)

    def test_delete_ingredient(self) -> None:
        """Удаление ингредиента"""
        ingredient = self.get_mock_ingredient()
        response = self.client.delete(f"{self.base_url}{ingredient.id}/")
        self.check_delete_response(response, Ingredients)


class StageAPITest(MockStages):
    base_url = "/api/stages/"

    def test_create_stage(self) -> None:
        pass

    def test_update_stage(self) -> None:
        pass

    def test_list_stages(self) -> None:
        """Получение списка стадий"""
        recipe = self.get_mock_recipe()
        stage_list = [
            self.get_mock_stage(recipe, {"order": 1}),
            self.get_mock_stage(recipe, {"order": 2}),
            self.get_mock_stage(recipe, {"order": 3}),
        ]
        response = self.client.get(self.base_url)
        self.check_list_response(response, 3)

    def test_delete_stage(self) -> None:
        """Удаление стадии"""
        stage = self.get_mock_stage()
        response = self.client.delete(f"{self.base_url}{stage.id}/")
        self.check_delete_response(response, Stages)

    # def test_reorder_stages(self) -> None:
    #     """Перераспределение стадий"""
    #     recipe = self.get_mock_recipe()
    #     stage_list: list[Stages] = [
    #         self.get_mock_stage(recipe, {"order": 1}),
    #         self.get_mock_stage(recipe, {"order": 2}),
    #         self.get_mock_stage(recipe, {"order": 3}),
    #     ]
    #     response = self.client.post(
    #         f"{self.base_url}reorder/",
    #         {
    #             "recipe_id": recipe.id,
    #             "start_order": 2,
    #         },
    #     )
    #     try:
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     except AssertionError as e:
    #         logger.error("Generated response: %s", response.data)
    #         raise e
    #     response = self.client.get(self.base_url)
    #     stage_result = response.data["results"][1:]
    #     for idx, stage in enumerate(stage_list[1:]):
    #         try:
    #             self.assertEqual(stage.order + 1, stage_result[idx]["order"])
    #         except AssertionError as e:
    #             logger.error("[%s] Expected order: %s", idx, stage.order + 1)
    #             logger.error(
    #                 "[%s] Calculated order: %s", idx, stage_result[idx]["order"]
    #             )
    #             raise e
