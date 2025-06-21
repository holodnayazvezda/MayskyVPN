import os
import platform


def get_env_python_command() -> str:
    if os.name == "nt":
        return r'.\.venv\Scripts\python'
    else:
        return './.venv/bin/python3'


def get_env_pip_command() -> str:
    if os.name == "nt":
        return r'.\.venv\Scripts\pip'
    else:
        return './.venv/bin/pip3'
