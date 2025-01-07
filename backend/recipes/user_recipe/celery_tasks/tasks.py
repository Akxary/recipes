import smtplib
from recipes.settings import SmtpConfig
from user_recipe.celery_tasks.celery_config import celery_app

@celery_app.task
def send_tmp_code_email():
    with smtplib.SMTP_SSL(SmtpConfig.HOST,SmtpConfig.PORT) as server:
            server.login(SmtpConfig.USER, SmtpConfig.PASS)
            server.send_message(msg_content)