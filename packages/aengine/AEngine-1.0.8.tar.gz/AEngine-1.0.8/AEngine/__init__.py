import rich
from AEngine.Data import String
import AEngine.settings
from AEngine.Files import File
import dotenv
import os

false = False
true = True

file = File("AEngine_info/changes.md")
file.create()
file.add(File(AEngine.settings.__source_path__ + "changes.md").read())


def print(*text, styles="", sep=" ", end="\n", file=None, flush=False):
    pre = f"[{styles}]"
    post = f"[/{styles}]"
    if pre == "[]":
        pre = post = ""
    to_print = []
    for i in text:
        to_print.append(pre + str(i) + post)
    rich.print(*to_print, sep=sep, end=end, file=file, flush=flush)


def set_font_path(path):
    dotenv.set_key(settings.__source_path__ + "/settings.env", "PATH_KEY", path)
