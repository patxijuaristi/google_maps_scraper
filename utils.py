import sys
import os

def resource_path(relative_path):
    """ To get resources path for creating the .exe with PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)