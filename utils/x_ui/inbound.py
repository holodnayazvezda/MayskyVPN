from py3xui import AsyncApi
import json
from py3xui.inbound import Inbound, Settings, Sniffing, StreamSettings

from data.config import X_UI_PANEL_PATH, X_UI_PANEL_USERNAME, X_UI_PANEL_PASSWORD
from data.constants import REALITY_SETTINGS_STRING
from utils.x_ui.keys_getter import get_public_and_private_key_for_reality_connection
from utils.x_ui.ports_parser import get_new_port

async def create_inbound(remark: str) -> int:
    # создаем объект api и логинимся
    api = AsyncApi(X_UI_PANEL_PATH, X_UI_PANEL_USERNAME, X_UI_PANEL_PASSWORD)
    await api.login()
    keys = await get_public_and_private_key_for_reality_connection(api.session)

    reality_settings = json.loads(REALITY_SETTINGS_STRING)
    reality_settings['privateKey'] = keys['privateKey']
    reality_settings['settings']['publicKey'] = keys['publicKey']
    # создаем подключение
    settings = Settings(decryption='none')
    sniffing = Sniffing(enabled=False)
    tcp_settings = {
        "acceptProxyProtocol": False,
        "header": {"type": "none"},
    }
    stream_settings = StreamSettings(security="reality", network="tcp", tcp_settings=tcp_settings, reality_settings=reality_settings)

    inbound = Inbound(
        enable=True,
        port=get_new_port(),
        protocol="vless",
        settings=settings,
        stream_settings=stream_settings,
        sniffing=sniffing,
        remark=remark,
    )

    await api.inbound.add(inbound)
    return await get_inbound_id(remark)


async def get_inbound_id(remark: str) -> int:
    # создаем объект api и логинимся
    api = AsyncApi(X_UI_PANEL_PATH, X_UI_PANEL_USERNAME, X_UI_PANEL_PASSWORD)
    await api.login()

    inbounds = await api.inbound.get_list()
    for inbound in inbounds:
        if inbound.remark == remark:
            return inbound.id
    return -1
