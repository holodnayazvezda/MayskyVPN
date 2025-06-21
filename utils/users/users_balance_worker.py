import sqlite3
from typing import Literal

from data.constants import BALANCE_DB_PATH


def init_db():
    conn = sqlite3.connect(BALANCE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS balances (
            user_id INTEGER PRIMARY KEY,
            rub_balance INTEGER DEFAULT 0,
            star_balance INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


def apply_change(diff: str) -> int:
    try:
        return int(diff)
    except ValueError:
        raise ValueError(f"Invalid diff format: {diff}")


def change_balance(user_id: int, diff: str, currency: Literal["rub", "star"]):
    conn = sqlite3.connect(BALANCE_DB_PATH)
    cursor = conn.cursor()

    delta = apply_change(diff)

    cursor.execute("SELECT rub_balance, star_balance FROM balances WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    if not row:
        rub_balance = delta if currency == "rub" else 0
        star_balance = delta if currency == "star" else 0
        cursor.execute(
            "INSERT INTO balances (user_id, rub_balance, star_balance) VALUES (?, ?, ?)",
            (user_id, rub_balance, star_balance)
        )
    else:
        current_rub, current_star = row
        if currency == "rub":
            new_rub = current_rub + delta
            cursor.execute("UPDATE balances SET rub_balance = ? WHERE user_id = ?", (new_rub, user_id))
        else:
            new_star = current_star + delta
            cursor.execute("UPDATE balances SET star_balance = ? WHERE user_id = ?", (new_star, user_id))

    conn.commit()
    conn.close()


def change_rub_balance(user_id: int, diff: str):
    change_balance(user_id, diff, currency="rub")


def change_star_balance(user_id: int, diff: str):
    change_balance(user_id, diff, currency="star")


def get_rub_balance(user_id: int) -> int:
    conn = sqlite3.connect(BALANCE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT rub_balance FROM balances WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else 0


def get_star_balance(user_id: int) -> int:
    conn = sqlite3.connect(BALANCE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT star_balance FROM balances WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else 0
