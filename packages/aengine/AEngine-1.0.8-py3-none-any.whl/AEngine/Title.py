import shutil


class Title:
    def __init__(self, text, template="=", sep=None, color="white", gap=" "):
        if sep is None:
            sep = ["(", ")"]
        self.text = text
        self.s_template = template
        if len(sep) > 1:
            self.l_sep = sep[0]
            self.r_sep = sep[1]
        else:
            self.l_sep = self.r_sep = sep
        self.size = shutil.get_terminal_size().columns
        self.color = color
        self.gap = gap

    def __str__(self):
        half_text_length = len(self.text) // 2
        half = self.size // 2 - half_text_length - len(self.gap) - (len(self.text) - half_text_length * 2) - len(self.l_sep) - len(self.r_sep)
        h = half // len(self.s_template)
        left = f"{self.s_template * h + self.s_template[:(half - h)]}{self.l_sep}{self.gap}"
        right = f"{self.gap}{self.r_sep}{self.s_template * h + self.s_template[:(half - h)]}"

        return f"[{self.color}]{left}[/{self.color}]{self.text}[{self.color}]{right}[/{self.color}]"
