import asyncio
import os.path
import subprocess

import requests
from data.startup_texts import *
from utils.files.get_env_python_path import get_env_python_command

process = None


async def start_server(sleep_after_request: int, stop_error_count: int) -> None:
    global process

    error_count = 0
    is_working = True
    process = subprocess.Popen([get_env_python_command(), './main.py'])
    print(f'{BotStarted}')
    while True:
        try:
            status = requests.get("https://api.telegram.org/").status_code
        except Exception:
            status = 100
        if status != 200:
            error_count += 1
            if error_count >= stop_error_count and is_working:
                print(f'WARNING! The number of errors exceeded {stop_error_count}.')
                print(f'{BotStopped}')
                process.kill()
                is_working = False
        else:
            error_count = 0
            if not is_working:
                is_working = True
                process = subprocess.Popen([get_env_python_command(), './main.py'])
                print(f'{BotRestarted}')
        await asyncio.sleep(sleep_after_request)


if __name__ == '__main__':
    try:
        if not os.path.exists('data/databases'):
            os.makedirs('data/databases')
        asyncio.run(start_server(3, 2))
    except KeyboardInterrupt:
        if process:
            process.kill()
        print(f'{BotStopped}')