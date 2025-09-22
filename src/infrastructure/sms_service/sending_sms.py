import smsaero

from src.config.settings import Config


async def send_number(number, code):
    sms_email = Config.SMS_AERO_USER
    sms_api_key = Config.SMS_AERO_API_KEY
    message = f"{code} {Config.SMS_AERO_CONFIRMATION_NUMBER}"
    sms_api = smsaero.SmsAero(sms_email, sms_api_key)
    try:
        result = await sms_api.send_sms(int(number), message)
        if result["status"] == 8:
            return True
        else:
            return False

    # except Exception as exc:
    #     return False
    finally:
        await sms_api.close_session()

