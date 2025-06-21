import sqlite3
import asyncio

from data.config import INBOUNDS_DATA
from utils.x_ui.inbound import create_inbound
from utils.x_ui.user import create_user


async def check_inbounds_table_exists(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS inbouds (remark TEXT UNIQUE, id INTEGER);")
    cursor.execute("SELECT id FROM inbouds;")
    all_inbounds_ids = list(map(lambda el: el[0], cursor.fetchall()))
    if len(all_inbounds_ids) != 0:
        print("Все inbounds уже созданы")
        return
    await create_inbounds_and_insert(db_path)


async def create_inbounds_and_insert(db_path: str) -> None:
    print('Создание inbounds и вставка в базу данных...')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("BEGIN TRANSACTION;")
    insert_query = "INSERT INTO inbouds (remark, id) VALUES (?, ?);"
    inbounds_remarks = ['Пробный период'] + list(map(lambda el: el['remark'], INBOUNDS_DATA.values()))
    for remark in inbounds_remarks:
        inbound_id = await create_inbound(remark)
        await create_user(inbound_id, f'admin {remark}', 0)
        cursor.execute(insert_query, (remark, inbound_id))
        print(f'Создана inbound {remark}')
        await asyncio.sleep(0.5)
    conn.commit()
    print('Inbounds успешно созданы и вставлены в базу данных.')
