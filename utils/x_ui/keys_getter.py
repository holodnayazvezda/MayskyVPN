import requests
import json
from data.config import X_UI_PANEL_PATH


async def get_public_and_private_key_for_reality_connection(access_token: str) -> dict:
    r = requests.post(
        f'{X_UI_PANEL_PATH}server/getNewX25519Cert',
        cookies={'3x-ui': access_token, 'lang': 'ru-RU'},
    )
    keys = r.json()['obj']
    return keys