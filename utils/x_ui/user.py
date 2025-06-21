import uuid

from py3xui import AsyncApi, Api
from py3xui import Client

from data.config import X_UI_PANEL_PATH, X_UI_PANEL_USERNAME, X_UI_PANEL_PASSWORD

async def create_user(
        inbound_id: int, email: str, tg_id: int,
        expiry_time: int = 0, limit_ip: int = 0, total_gb: int = 0
) -> str:
    # создаем объект api и логинимся
    api = AsyncApi(X_UI_PANEL_PATH, X_UI_PANEL_USERNAME, X_UI_PANEL_PASSWORD)
    await api.login()
    # создаем пользователя
    client_id = str(uuid.uuid4())
    new_client = Client(
        id=client_id,
        email=email,
        enable=True,
        tg_id=tg_id,
        expiry_time=expiry_time,
        limit_ip=limit_ip,
        total_gb=total_gb
    )
    # добавляем в бд
    await api.client.add(inbound_id, [new_client] )
    return client_id


def delete_user(
        inbound_id: int, client_id: str
) -> None:
    # создаем объект api и логинимся
    api = Api(X_UI_PANEL_PATH, X_UI_PANEL_USERNAME, X_UI_PANEL_PASSWORD)
    api.login()
    # удаляем пользователя
    api.client.delete(
        inbound_id=inbound_id,
        client_uuid=client_id
    )
