from utils.users.referral_users_worker import init_db as referral_init_db
from utils.users.users_balance_worker import init_db as balance_init_db
from utils.users.users_connections_worker import init_db as connection_init_db


def init_databases():
    referral_init_db()
    balance_init_db()
    connection_init_db()