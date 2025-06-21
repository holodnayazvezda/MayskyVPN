from py3xui import AsyncApi

from data.config import X_UI_PANEL_PATH, X_UI_PANEL_USERNAME, X_UI_PANEL_PASSWORD, X_UI_HOST


async def generate_config_string(inbound_id: int, user_uuid: str, user_email: str) -> str:
    api = AsyncApi(X_UI_PANEL_PATH, X_UI_PANEL_USERNAME, X_UI_PANEL_PASSWORD)
    await api.login()

    inbound = await api.inbound.get_by_id(inbound_id)
    public_key = inbound.stream_settings.reality_settings.get("settings").get("publicKey")
    website_name = inbound.stream_settings.reality_settings.get("serverNames")[0]
    short_id = inbound.stream_settings.reality_settings.get("shortIds")[0]

    connection_string = (
        f"vless://{user_uuid}@{X_UI_HOST}:{inbound.port}"
        f"?type=tcp&security=reality&pbk={public_key}&fp=firefox&sni={website_name}"
        f"&sid={short_id}&spx=%2F#{inbound.remark}-{user_email}"
    )

    return connection_string
