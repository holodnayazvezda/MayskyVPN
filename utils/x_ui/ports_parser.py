import os

from random import randint


def get_new_port() -> int:
    if not os.path.exists('data/conf_files/used_ports.txt'):
        os.makedirs('data/conf_files', exist_ok=True)
        with open('data/conf_files/used_ports.txt', 'w') as file:
            file.write('')

    f = open('data/conf_files/used_ports.txt', 'r', encoding='utf-8')
    ports = f.readlines()
    f.close()

    new_port = randint(1024, 65535)
    while str(new_port) in ports:
        new_port = randint(1024, 65535)

    f = open('data/conf_files/used_ports.txt', 'a', encoding='utf-8')
    f.write(f'{new_port}\n')
    f.close()

    return new_port
