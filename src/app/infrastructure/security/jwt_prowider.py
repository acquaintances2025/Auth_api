import jwt

from app.config.settings import Config

async  def create_access_token(uuid_user):
    access_token = jwt.encode({"exp": Config.EXP_ACCESS_TOKEN,"uuid_user": str(uuid_user)}, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return access_token

async def create_refresh_token(uuid_user):
    refresh_token = jwt.encode({"exp": Config.EXP_REFRESH_TOKEN,"uuid_user": str(uuid_user)}, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return refresh_token

async def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        return payload, True
    except jwt.ExpiredSignatureError:
        return None, False
    except Exception:
        return None, False
