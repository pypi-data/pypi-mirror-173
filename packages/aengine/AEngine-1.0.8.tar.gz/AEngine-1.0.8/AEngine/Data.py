from enum import Enum
import shutil
import random


class Obj(dict):
    __default = None

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            if isinstance(args[0], dict):
                for k, v in args[0].items():
                    self.__dict__[k] = v
        for k, v in kwargs.items():
            self.__dict__[k] = v

        super().__init__(self.__dict__)

    def __str__(self):
        s = ""
        dct = self.__dict__.copy()
        if "_Obj__default" in list(dct):
            del dct["_Obj__default"]
        for i in list(dct):
            s += f"{i} => {dct[i]}, "
        s = s[:-2]
        return f"AEngine.Obj({s})"

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            return self.default

    def __getattr__(self, item):
        try:
            return self.__dict__["item"]
        except KeyError:
            return self.default

    def extend(self, _dict: dict):
        for k, v in _dict.items():
            super().__setitem__(k, v)
            self.__setattr__(k, v)
        self.update()

    @property
    def default(self):
        return self.__default

    @default.setter
    def default(self, value):
        self.__default = value

    def get(self, value):
        return self.__getitem__(value)


class Chain:
    def __init__(self, *llist):
        if len(llist) == 1 and isinstance(llist[0], list):
            llist = llist[0]
        if llist is None:
            llist = []
        self.__list = llist

        for i in range(len(self.__list) - 1):
            self.__dict__[self.__list[i]] = self.__list[i + 1]

        self.__dict__[self.__list[-1]] = self.__list[0]

    def __str__(self):
        s = ""
        dct = self.__dict__.copy()
        del dct["_Chain__list"]
        for i in list(dct):
            s += f"{i} => {dct[i]}, "
        s = s[:-2]
        return f"AEngine.Chain({s})"

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self.__dict__[item]

    def __update(self):
        for i in range(len(self.__list) - 1):
            self.__dict__[self.__list[i]] = self.__list[i + 1]

        self.__dict__[self.__list[-1]] = self.__list[0]

    def pop(self, index):
        del self.__dict__[index]
        self.__list.pop(self.__list.index(index))
        self.__update()

    def index(self, value):
        return self.__list[self.__list.index(value) - 1]

    def __iter__(self):
        for i in self.__list:
            yield self[i]


class Align(Enum):
    Start = 0
    Center = 1
    End = 2


class String:
    __align = None

    def __init__(self, string, align=Align.Start, color="white"):
        self.aligns = {
            Align.Start: self.__left,
            Align.Center: self.__center,
            Align.End: self.__right
        }
        self.__string = string
        self.string = string
        self.color = color
        self.align = align

    def __center(self):
        s = self.string.split("\n")
        self.string = ""
        prefix = f"[{self.color}]"
        postfix = f"[/{self.color}]"
        for i in s:
            self.string += prefix + i.center(shutil.get_terminal_size().columns) + postfix + "\n"

    def __left(self):
        prefix = f"[{self.color}]"
        postfix = f"[/{self.color}]"
        self.string: str = prefix + self.__string + postfix

    def __right(self):
        size = shutil.get_terminal_size().columns
        s = self.string.split("\n")
        self.string = ""
        prefix = f"[{self.color}]"
        postfix = f"[/{self.color}]"
        for i in s:
            self.string += prefix + str(size * " ")[:-len(i)] + i + postfix + "\n"

    @property
    def align(self):
        return self.__align

    @align.setter
    def align(self, value):
        self.aligns[value]()
        self.__align = value

    def add_align(self, key, func):
        self.aligns[key] = func

    def replace(self, old, new):
        return self.__string.replace(old, new)

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

    def __len__(self):
        return len(self.__string)


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_int(self):
        self.x = int(self.x)
        self.y = int(self.y)

    def __add__(self, other):
        x = self.x
        y = self.y
        if isinstance(other, Vector2):
            x += other.x
            y += other.y

        elif isinstance(other, int) or isinstance(other, float):
            x += other
            y += other

        else:
            raise ValueError(f"invalid operand for +: '{type(self)}' and '{type(other)}'")

        return Vector2(x, y)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        x = self.x
        y = self.y
        if isinstance(other, Vector2):
            x *= other.x
            y *= other.y

        elif isinstance(other, int) or isinstance(other, float):
            x *= other
            y *= other

        else:
            raise ValueError(f"invalid operand for *: '{type(self)}' and '{type(other)}'")

        return Vector2(x, y)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        x = self.x
        y = self.y
        if isinstance(other, Vector2):
            x /= other.x
            y /= other.y

        elif isinstance(other, int) or isinstance(other, float):
            x /= other
            y /= other

        else:
            raise ValueError(f"invalid operand for /: '{type(self)}' and '{type(other)}'")

        return Vector2(x, y)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __sub__(self, other):
        x = self.x
        y = self.y
        if isinstance(other, Vector2):
            x -= other.x
            y -= other.y

        elif isinstance(other, int) or isinstance(other, float):
            x -= other
            y -= other

        else:
            raise ValueError(f"invalid operand for /: '{type(self)}' and '{type(other)}'")

        return Vector2(x, y)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __repr__(self):
        return f"AEngine.Vector2({self.x}, {self.y})"

    def __str__(self):
        return repr(self)

    def __int__(self):
        return int(self.x + self.y)

    def to_list(self):
        return [self.x, self.y]

    @classmethod
    @property
    def up(self):
        return Vector2(0, 1)

    @classmethod
    @property
    def down(self):
        return Vector2(0, -1)

    @classmethod
    @property
    def left(self):
        return Vector2(-1, 0)

    @classmethod
    @property
    def right(self):
        return Vector2(1, 0)

    @classmethod
    @property
    def zero(self):
        return Vector2(0, 0)

    @classmethod
    def random(cls, rng=None):
        if rng is None:
            rng = [-999_999_999_999, 999_999_999_999]
        return Vector2(random.randrange(rng[0], rng[1]), random.randrange(rng[0], rng[1]))

    def __iter__(self):
        yield self.x
        yield self.y
