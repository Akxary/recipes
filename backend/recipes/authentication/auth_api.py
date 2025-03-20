import logging
from random import randint
from email.mime.text import MIMEText
from recipes.settings import BASE_DIR, SmtpConfig
from celery_tasks.tasks import send_tmp_code_email
from authors.models import Authors
from redis_api.redis_api import RedisClient
from rest_framework_simplejwt.tokens import RefreshToken

from jinja2 import Environment, FileSystemLoader

jinja2_env = Environment(loader=FileSystemLoader(BASE_DIR/"user_recipe"/"templates"))
email_template = jinja2_env.get_template("email.html")
logger = logging.getLogger(__name__)

def send_verification_code(email: str) -> None:
    redis_client = RedisClient(email)
    tmp_code = str(randint(100_000, 999_999))
    redis_client.set_current_author_temporary_code(tmp_code)
    email_content = MIMEText(email_template.render(
        email=email,
        app_name="Recipes",
        verification_code=tmp_code,
        lifetime=redis_client.Auth.TMP_CODE_TIME,
    ), _subtype="html")
    email_content['Subject'] = "Код авторизации"
    email_content['From'] = SmtpConfig.USER
    email_content['To'] = email
    send_tmp_code_email.apply_async(args=[email_content.as_bytes(), email])


def verify_code(email: str, code: str) -> bool:
    redis_client = RedisClient(email)
    return redis_client.check_current_author_temporary_code(code)


def set_token(email: str) -> dict[str, str]:
    author, created = Authors.objects.get_or_create({"email": email})
    logger.info("%s author: %s", "Created" if created else "Got",author)
    refresh = RefreshToken.for_user(author)
    refresh["email"] = email
    logger.info("Set refresh token for author: %s", refresh)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

