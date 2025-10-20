import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config.settings import Config
from ..loggings.logger import logger


async def send_email(user_email, code):
    """
    Отправка сообщения пользователю
    """
    msg = MIMEMultipart()
    msg['From'] = os.getenv("MAIL_SERVICE_USER")
    msg['To'] = user_email

    msg['Subject'] = "Код подтверждения."
    email_body = f"Ваш код подтверждения: {str(code)}"
    msg.attach(MIMEText(email_body, 'html'))

    try:
        with smtplib.SMTP(Config.MAIL_SERVICE_ADRESS, Config.MAIL_SERVICE_PORT) as server:
            server.starttls()
            server.login (Config.MAIL_SERVICE_USER, Config.MAIL_SERVICE_PASS)
            server.send_message(msg)
            logger.info(f"Письмо с кодом подтверждения успешно отправлено на {user_email}")
            return True
    except Exception as e:
        logger.info(f'Произошла ошибка при отправке письма: {e}')
        return False