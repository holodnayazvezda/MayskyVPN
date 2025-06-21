import sqlite3

from data.constants import REFERRAL_USERS_DB_PATH


def init_db():
    conn = sqlite3.connect(REFERRAL_USERS_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            referrer_id INTEGER,
            referred_count INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referrer_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def register_user(user_id, referrer_id=None):
    conn = sqlite3.connect(REFERRAL_USERS_DB_PATH)
    cursor = conn.cursor()

    # Проверка, зарегистрирован ли пользователь
    cursor.execute("SELECT id FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone():
        conn.close()
        return False  # уже зарегистрирован

    internal_referrer_id = None
    if referrer_id and referrer_id != user_id:  # нельзя пригласить самого себя
        cursor.execute("SELECT id FROM users WHERE user_id=?", (referrer_id,))
        row = cursor.fetchone()
        if row:
            internal_referrer_id = row[0]
            # Увеличение счётчика у пригласившего
            cursor.execute(
                "UPDATE users SET referred_count = referred_count + 1 WHERE id=?",
                (internal_referrer_id,)
            )

    cursor.execute('''
        INSERT INTO users (user_id, referrer_id)
        VALUES (?, ?)
    ''', (user_id, internal_referrer_id))

    conn.commit()
    conn.close()
    return True  # успешно зарегистрирован


def get_referred_count(user_id):
    conn = sqlite3.connect(REFERRAL_USERS_DB_PATH)
    cursor = conn.cursor()

    # Находим внутренний ID пользователя
    cursor.execute("SELECT id FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return 0  # пользователь не найден - значито никого не риглащал

    internal_id = row[0]
    # Получаем количество приглашённых
    cursor.execute("SELECT COUNT(*) FROM users WHERE referrer_id=?", (internal_id,))
    count = cursor.fetchone()[0]

    conn.close()
    return count

