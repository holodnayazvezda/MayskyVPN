import os
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

# Конфигурация XUI
X_UI_HOST = os.getenv("X_UI_HOST")
X_UI_PANEL_PATH = os.getenv("X_UI_PANEL_PATH")
X_UI_PANEL_USERNAME = os.getenv("X_UI_PANEL_USERNAME")
X_UI_PANEL_PASSWORD = os.getenv("X_UI_PANEL_PASSWORD")

# Redis
REDIS_URL = os.getenv("REDIS_URL")
AIOGRAM_REDIS_STORAGE = RedisStorage.from_url(
    url=REDIS_URL,
    connection_kwargs={'decode_responses': True}
)

# Бот токены
TOKENS = [
    os.getenv("BOT_MAIN_TOKEN_1"),
    os.getenv("BOT_MAIN_TOKEN_2"),
    os.getenv("BOT_MAIN_TOKEN_3"),
    os.getenv("BOT_MAIN_TOKEN_4"),
    os.getenv("BOT_MAIN_TOKEN_5")
]

PAYMENT_TOKENS = {
    os.getenv("BOT_MAIN_TOKEN_1"): os.getenv("BOT_PAYMENT_TOKEN_1"),
    os.getenv("BOT_MAIN_TOKEN_2"): os.getenv("BOT_PAYMENT_TOKEN_2"),
    os.getenv("BOT_MAIN_TOKEN_3"): os.getenv("BOT_PAYMENT_TOKEN_3"),
    os.getenv("BOT_MAIN_TOKEN_4"): os.getenv("BOT_PAYMENT_TOKEN_4"),
    os.getenv("BOT_MAIN_TOKEN_5"): os.getenv("BOT_PAYMENT_TOKEN_5"),

    os.getenv("BOT_TEST_TOKEN"): os.getenv("BOT_TEST_PAYMENT_TOKEN")
}

TEST_TOKENS = [
    os.getenv("BOT_TEST_TOKEN")
]

# Прочее
BACK_TO_MAIN_MENU_BUTTON_TEXT = '↩️ Назад в главное меню'
START_BUTTONS = ['📶 Мое подключение', '👤 Личный кабинет', 'ℹ️ Инструкция по использованию']

TRIAL_DURATION = 14
STARS_FOR_REFERRAL = 20

INBOUNDS_DATA = {
    '1_1': {'remark': '1 IP 1 месяц', 'price_rubles': 100, 'price_stars': 80},
    '3_1': {'remark': '3 IP 1 месяц', 'price_rubles': 200, 'price_stars': 160},
    '10_1': {'remark': '10 IP 1 месяц', 'price_rubles': 300, 'price_stars': 240},

    '1_3': {'remark': '1 IP 3 месяца', 'price_rubles': 250, 'price_stars': 200},
    '3_3': {'remark': '3 IP 3 месяца', 'price_rubles': 500, 'price_stars': 400},
    '10_3': {'remark': '10 IP 3 месяца', 'price_rubles': 750, 'price_stars': 600},

    '1_6': {'remark': '1 IP 6 месяцев', 'price_rubles': 450, 'price_stars': 360},
    '3_6': {'remark': '3 IP 6 месяцев', 'price_rubles': 900, 'price_stars': 720},
    '10_6': {'remark': '10 IP 6 месяцев', 'price_rubles': 1300, 'price_stars': 1000},

    '1_12': {'remark': '1 IP 12 месяцев', 'price_rubles': 800, 'price_stars': 640},
    '3_12': {'remark': '3 IP 12 месяцев', 'price_rubles': 1500, 'price_stars': 1200},
    '10_12': {'remark': '10 IP 12 месяцев', 'price_rubles': 2300, 'price_stars': 1800}
}

PRICES_IN_RUBLES = [
    100, 250, 450, 750,
    200, 500, 900, 1500,
    300, 750, 1300, 2300
]
PRICES_IN_STARS = [
    80, 200, 360, 600,
    160, 400, 720, 1200,
    240, 600, 1040, 1800
]
