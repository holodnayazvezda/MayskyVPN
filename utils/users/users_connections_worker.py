import sqlite3
import time
from data.constants import USERS_CONNECTIONS_DB_PATH
from utils.users.users_with_expired_keys_procesor import process_users_with_expired_keys


def init_db() -> None:
    conn = sqlite3.connect(USERS_CONNECTIONS_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_connections (
            chat_id INTEGER,
            bot_token TEXT,
            inbound_id INTEGER,
            client_id TEXT,
            expiry_timestamp INTEGER,
            connection_type TEXT,
            limit_ip INTEGER,
            key TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_user_to_connections_db(
    chat_id: int,
    bot_token: str,
    inbound_id: int,
    client_id: str,
    expiry_timestamp: int,
    connection_type: str,
    limit_ip: int,
    key: str
) -> None:
    # уменьшаем реальный интервал на 2 часа
    expiry_timestamp -= 2 * 60 * 60 * 1000

    conn = sqlite3.connect(USERS_CONNECTIONS_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users_connections (
            chat_id, bot_token, inbound_id, client_id,
            expiry_timestamp, connection_type, limit_ip, key
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        chat_id, bot_token, inbound_id, client_id,
        expiry_timestamp, connection_type, limit_ip, key
    ))
    conn.commit()
    conn.close()


def remove_expired_users() -> None:
    now_ms = int(time.time() * 1000)

    conn = sqlite3.connect(USERS_CONNECTIONS_DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
                   SELECT chat_id, bot_token, inbound_id, client_id
                   FROM users_connections
                   WHERE expiry_timestamp < ?
                   ''', (now_ms,))
    expired_users = cursor.fetchall()

    cursor.execute('''
        DELETE FROM users_connections WHERE expiry_timestamp < ?
    ''', (now_ms,))
    conn.commit()
    conn.close()

    process_users_with_expired_keys(expired_users)
