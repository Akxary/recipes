import logging
from typing import TypeVar
from django.db.models import Model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

logger = logging.getLogger(__name__)

BASE_MODEL = TypeVar(
    "BASE_MODEL",
    # type[Authors],
    # type[Recipes],
    # type[Ingredients],
    # type[Stages],
    bound=type[Model],
)


class CheckResponse(APITestCase):
    def check_single_response(
        self,
        response: Response,
        expected_status: int,
        expected_data: dict,
    ) -> None:
        try:
            self.assertEqual(response.status_code, expected_status)
            for f_name, f_value in expected_data.items():
                self.assertEqual(response.data[f_name], f_value)
        except AssertionError as e:
            logger.error("Generated response: %s", response.data)
            logger.error("Expected data: %s", expected_data)
            raise e

    def check_list_response(
        self,
        response: Response,
        expected_len: int,
        expected_status: int = status.HTTP_200_OK,
    ) -> None:
        try:
            self.assertEquals(response.status_code, expected_status)
            self.assertEquals(response.data["count"], expected_len)
        except AssertionError as e:
            logger.error("Generated response: %s", response.data)
            raise e

    def check_delete_response(
        self,
        response: Response,
        model: BASE_MODEL,
        expected_status: int = status.HTTP_204_NO_CONTENT,
        expected_len: int = 0,
    ) -> None:
        try:
            self.assertEqual(response.status_code, expected_status)
            self.assertEqual(len(model.objects.all()), expected_len)
        except AssertionError as e:
            logger.error("Generated repsonse: %s", response.data)
            raise e