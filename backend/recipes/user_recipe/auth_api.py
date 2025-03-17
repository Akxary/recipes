from random import randint
from email.mime.text import MIMEText
from recipes.settings import BASE_DIR, SmtpConfig
from user_recipe.celery_tasks.tasks import send_tmp_code_email
from user_recipe.models import Authors
from user_recipe.redis_api import RedisClient

from jinja2 import Environment, FileSystemLoader

jinja2_env = Environment(loader=FileSystemLoader(BASE_DIR/"user_recipe"/"templates"))
email_template = jinja2_env.get_template("email.html")


def send_verification_code(author: Authors) -> None:
    redis_client = RedisClient(author.id)
    tmp_code = str(randint(100_000, 999_999))
    redis_client.set_current_author_temporary_code(tmp_code)
    email_content = MIMEText(email_template.render(
        email=author.email,
        app_name="Recipes",
        verification_code=tmp_code,
        lifetime=redis_client.Auth.TMP_CODE_TIME,
    ), _subtype="html")
    email_content['Subject'] = "Код авторизации"
    email_content['From'] = SmtpConfig.USER
    email_content['To'] = author.email
    send_tmp_code_email.apply_async(args=[email_content.as_bytes(), author.email])


def verify_code(author: Authors, code: str) -> bool:
    redis_client = RedisClient(author.id)
    return redis_client.check_current_author_temporary_code(code)


def set_token(author: Authors) -> tuple[str, str]:
    return "", ""