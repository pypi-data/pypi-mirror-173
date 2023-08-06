__all__ = ["Banner"]

from functools import lru_cache
from AEngine.settings import __source_path__


class BannerString:
    def __init__(self, string="", size=0):
        self.lines = ["" for _ in range(size)]
        if string:
            lines = string.split("\n")
            self.lines[len(self.lines) - len(lines):len(self.lines)] = lines

    def __add__(self, other):
        res = ''
        mx = 0
        if isinstance(other, BannerString):
            length = max(list(map(lambda x: len(x), self.lines)))
            for i, line in enumerate(other.lines):
                ln = self.lines[i] + " " * (length - len(self.lines[i])) + line + " \n"
                if len(ln) > mx:
                    mx = len(ln)
                res += ln
            res = "\n".join(list(map(lambda x: x + " " * (mx - len(x)), res.split('\n'))))
        return BannerString(res)

    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        return "\n".join(self.lines)

    def __repr__(self):
        return str(self)


class Banner:
    __letters = []

    @classmethod
    @lru_cache
    def from_string(cls, string):
        buffer = {}
        string = string.replace(" ", "_")
        for letter in string:
            letter = letter.replace("_", "space")
            letter = letter.replace("*", "star")
            letter = letter.replace(".", "dot")
            letter = letter.replace(";", "semicolon")
            letter = letter.replace(",", "comma")
            letter = letter.replace("?", "question_mark")
            letter = letter.replace("!", "exclamation_mark")
            letter = letter.replace("&", "ampersand")
            letter = letter.replace("/", "slash")
            letter = letter.replace("(", "l_bracket")
            letter = letter.replace(")", "r_bracket")
            letter = letter.replace(":", "colon")
            if not (letter in list(buffer)):
                if letter.isupper():
                    letter = "_" + letter
                with open(__source_path__ + "alphabet/" + letter, "r") as file:
                    let = file.read().strip("\n").strip("%")
                    buffer[letter] = let
            else:
                let = buffer[letter]
            cls.__letters.append(BannerString(let, size=6))
        res = BannerString(size=6)
        for i in cls.__letters:
            res += i

        return str(res)
