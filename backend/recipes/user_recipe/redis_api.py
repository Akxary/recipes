from contextlib import contextmanager
from typing import Generator, ContextManager
from redis import Redis
from recipes.settings import RedisConfig


class RedisClient:

    @contextmanager
    def get_connection(self) -> Generator[Redis, None, None]:
        try:
            client = Redis(
                host=RedisConfig.HOST,
                port=RedisConfig.PORT,
                db=RedisConfig.DB,
            )
            yield client
        finally:
            client.close()

    def get_recipe_like_count(self, recipe_id: int) -> int:
        with self.get_connection() as client:
            return client.scard(
                RedisConfig.join(
                    RedisConfig.RECIPE_SET_NAME,
                    recipe_id,
                )
            )
    
    def is_current_author_like(self,prefix: str, prefix_id:int, author_id: int) -> bool:
        with self.get_connection() as client:
            return client.sismember(
                RedisConfig.join(
                    prefix,
                    prefix_id,
                ),
                author_id
            )
        
    def is_current_author_like_recipe(self, recipe_id:int, author_id: int) -> bool:
        return self.is_current_author_like(RedisConfig.RECIPE_SET_NAME, recipe_id, author_id)
    
    def is_current_author_like_comment(self, recipe_id:int, author_id: int) -> bool:
        return self.is_current_author_like(RedisConfig.LIKE_SET_NAME, recipe_id, author_id)