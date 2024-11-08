import os


def get_absolute_path(path: str):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    new_path = os.path.normpath(script_dir)
    new_path = new_path.split(os.sep)
    path = path.split(os.sep)
    new_path.pop()
    new_path += path
    new_path = os.sep.join(new_path)
    return new_path
