import sqlite3

from data.constants import TRIAL_USERS_DB_PATH


async def remember_users_trial(user_id: int) -> None:
    conn = sqlite3.connect(TRIAL_USERS_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS trial_users (user_id INTEGER PRIMARY KEY);')
    cursor.execute("INSERT OR IGNORE INTO trial_users (user_id) VALUES (?);", (user_id,))
    conn.commit()
    conn.close()


async def can_use_trial(user_id: int) -> bool:
    conn = sqlite3.connect(TRIAL_USERS_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS trial_users (user_id INTEGER PRIMARY KEY);')
    cursor.execute("SELECT user_id FROM trial_users WHERE user_id = ?;", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is None