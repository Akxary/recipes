import smtplib
from random import randint

from user_recipe.models import Authors
from user_recipe.redis_api import RedisClient


def send_verification_code(author: Authors):
    redis_client = RedisClient(author.id)
    tmp_code = str(randint(100_000, 999_999))
    redis_client.set_current_author_temporary_code(tmp_code)
    