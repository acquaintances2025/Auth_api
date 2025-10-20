import jwt

from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, Optional, Any
from src.config.settings import Config
from ..loggings.logger import logger

async  def create_registration_access_token(user_id, user_role, email=None, phone=None):
    to_encode = {"user_id": user_id, "role": user_role, "email": email, "phone": phone}
    expires = datetime.utcnow() + timedelta(minutes=int(Config.EXP_ACCESS_TOKEN))
    to_encode.update({"exp": expires, "user_id": user_id})
    access_token = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return access_token


async  def create_access_token(user_id, user_role):
    to_encode = {"user_id": user_id, "role": user_role}
    expires = datetime.utcnow() + timedelta(minutes=int(Config.EXP_ACCESS_TOKEN))
    to_encode.update({"exp": expires, "user_id": user_id})
    access_token = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return access_token


async def create_refresh_token(user_id, user_role):
    to_encode = {"user_id": user_id, "role": user_role}
    expires = datetime.utcnow() + timedelta(minutes=int(Config.EXP_REFRESH_TOKEN))
    to_encode.update({"exp": expires, "user_id": user_id})
    refresh_token = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return refresh_token


async def decode_token(token) ->  Tuple[Optional[Dict[str, Any]], bool]:
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        return payload, True
    except jwt.ExpiredSignatureError:
        logger.warning("Срок действия токена истек")
        return None, False
    except Exception as e:
        logger.error(f"Ошибка при проверке токена: {e}")
        return None, False
