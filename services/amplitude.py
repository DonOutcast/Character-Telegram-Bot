import json
import logging

from settings import settings
from aiohttp import ClientSession


async def send_amplitude_event(aiohttp_session: ClientSession, event_type: str, user_id: int):
    headers = {
        "Content-Type": "application-json",
        "Accept": "*/*"
    }

    data = {
        "api_key": settings.amplitude_api_key,
        "events": [
            {
                "user_id": user_id,
                "event_type": event_type
            }
        ]
    }
    try:
        async with aiohttp_session.post(settings.amplitude_url, json=json.dumps(data), headers=headers) as response:
            if response.status == 200:
                logging.info("Событие успешно отправлено в Amplitude")
            else:
                logging.error("Ошибка при отправке события в Amplitude")
    except:
        pass