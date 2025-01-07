from contextlib import contextmanager
from dataclasses import dataclass
from datetime import timedelta
import time
from typing import Generator
from redis import Redis
from recipes.settings import RedisConfig


class RedisClient:

    @dataclass(frozen=True)
    class SetType:
        RECIPE_SET_NAME = "RECIPE_SET"
        LIKE_SET_NAME = "LIKE_SET"

    @dataclass(frozen=True)
    class Auth:
        TMP_CODE_NAME: str = "TMP_CODE"
        TMP_CODE_TIME: timedelta = timedelta(minutes=5)
        JWT_NAME: str = "JWT"
        JWT_TIME: timedelta = timedelta(days=7)

    def __init__(self, author_id: int)->None:
        self.author_id = author_id
    
    @staticmethod
    @contextmanager
    def get_connection() -> Generator[Redis, None, None]:
        try:
            client = Redis(
                host=RedisConfig.HOST,
                port=RedisConfig.PORT,
                db=RedisConfig.DB,
            )
            yield client
        finally:
            client.close()

    @staticmethod
    def _join(*subkeys: str | int) -> str:
        return "_".join(map(str, subkeys))

    @classmethod
    def get_recipe_like_count(cls, recipe_id: int) -> int:
        with cls.get_connection() as client:
            return client.scard(
                cls._join(
                    cls.SetType.RECIPE_SET_NAME,
                    recipe_id,
                )
            )

    def _is_current_author_like(
        self,
        prefix: str,
        prefix_id: int,
    ) -> bool:
        with self.get_connection() as client:
            return client.sismember(
                self._join(
                    prefix,
                    prefix_id,
                ),
                self.author_id,
            )

    def is_current_author_like_recipe(self, recipe_id: int) -> bool:
        return self._is_current_author_like(
            self.SetType.RECIPE_SET_NAME,
            recipe_id,
        )

    def is_current_author_like_comment(self, recipe_id: int) -> bool:
        return self._is_current_author_like(
            self.SetType.LIKE_SET_NAME,
            recipe_id,
        )

    def _get_current_code_by_name(self, prefix: str) -> str | None:
        with self.get_connection() as client:
            code = client.get(self._join(prefix, self.author_id))
            if code:
                return str(code)
            return None

    def _set_current_author_token(self, prefix: str, token: str, token_lifetime: timedelta) -> None:
        with self.get_connection() as client:
            client.set(self._join(prefix, self.author_id), token, token_lifetime)

    def set_current_author_temporary_code(self, code: str) -> None:
        self._set_current_author_token(self.Auth.TMP_CODE_NAME, code, self.Auth.TMP_CODE_TIME)
    
    def check_current_author_temporary_code(self, code: str) -> bool:
        return self._get_current_code_by_name(self.Auth.TMP_CODE_NAME) == code
    
    def set_current_author_jwt(self, jwt: str) -> None:
        self._set_current_author_token(self.Auth.JWT_NAME, jwt, self.Auth.JWT_TIME)

    def check_current_author_jwt(self, jwt: str) -> bool:
        return self._get_current_code_by_name(self.Auth.JWT_NAME) == jwt
