import os


def safe_remove_files(*files):
    for file in files:
        try:
            os.remove(file)
        except OSError:
            pass
