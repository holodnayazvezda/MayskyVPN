def get_text_and_format_it(filename: str, *args) -> str:
    f = open(file=filename, mode='r+', encoding='utf-8')
    message_text = f.read().format(*args)
    f.close()
    return message_text
