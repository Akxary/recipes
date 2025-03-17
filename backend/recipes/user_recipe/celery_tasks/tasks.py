import smtplib
from smtplib import SMTP_SSL
from recipes.settings import SmtpConfig
from user_recipe.celery_tasks.celery_config import celery_app

@celery_app.task
def send_tmp_code_email(msg_bytes: bytes, to_email: str):
    with smtplib.SMTP_SSL(SmtpConfig.HOST,SmtpConfig.PORT) as server:
        server.login(SmtpConfig.USER, SmtpConfig.PASS)
        server.sendmail(from_addr=SmtpConfig.USER, to_addrs=to_email, msg=msg_bytes)
