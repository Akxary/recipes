from django.test import TestCase
from rest_framework import status

from authors.models import Authors
from recipes.check_utils import CheckResponse


class MockAuthor(CheckResponse):
    def get_mock_author(self, sub_data: dict | None = None) -> Authors:
        data = {"author_name": "Bob", "email": "Bob@example.com"}
        if sub_data:
            data.update(sub_data)
        return Authors.objects.create(**data)


class AuthorAPITestCase(MockAuthor):
    base_url = "/api/authors/"

    def test_create_author(self) -> None:
        """Тестируем создание автора"""
        data = {"author_name": "Bob", "email": "bob@example.com"}
        response = self.client.post(self.base_url, data)
        self.check_single_response(response, status.HTTP_201_CREATED, data)

    def test_list_authors(self) -> None:
        """Тестируем получения списка авторов"""
        list_authors = [
            self.get_mock_author(),
            self.get_mock_author(
                {
                    "author_name": "Alice",
                    "email": "Alice@example.com",
                }
            ),
        ]
        response = self.client.get(self.base_url)
        self.check_list_response(response, len(list_authors))

    def test_update_author(self) -> None:
        """Тестируем обновление автора"""
        # TODO: проверить, что ид автора совпадает с обновляемым
        author = self.get_mock_author()
        data = {"author_name": "Alice"}
        response = self.client.patch(self.base_url + f"{author.id}/", data)
        self.check_single_response(response, status.HTTP_200_OK, data)

    def test_delete_author(self) -> None:
        """Тестируем удаление автора"""
        # TODO: проверить, что ид автора совпадает с удаляемым
        author = self.get_mock_author()
        response = self.client.delete(self.base_url + f"{author.id}/")
        self.check_delete_response(response, Authors)

# Create your tests here.
