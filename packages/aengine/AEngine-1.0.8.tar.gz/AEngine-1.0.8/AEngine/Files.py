import os


class File:
    def __init__(self, filename, encoding="utf-8"):
        self.filename = filename
        self.enc = encoding

    def read(self):
        with open(self.filename, 'r', encoding=self.enc) as file:
            return file.read()

    def add(self, text):
        with open(self.filename, 'a', encoding=self.enc) as file:
            file.write(text)
            file.close()

    def create(self):
        open(self.filename, 'w', encoding=self.enc)


class FileManager:
    @staticmethod
    def create_file(filename, encoding="utf-8"):
        with open(filename, 'w', encoding=encoding) as file:
            file.write('')
            file.close()

    @staticmethod
    def add(filename, text, encoding="utf-8"):
        with open(filename, 'a', encoding=encoding) as file:
            file.write(text)
            file.close()

    @staticmethod
    def rewrite(filename, text, encoding="utf-8"):
        with open(filename, 'w', encoding=encoding) as file:
            file.write(text)
            file.close()

    @classmethod
    def rename(cls, old_name, new_name, encoding="utf-8"):
        with open(old_name, 'r', encoding=encoding) as file:
            content = file.read()
            file.close()

        cls.create_file(new_name)
        cls.add(new_name, content)

        os.remove(old_name)

    @staticmethod
    def read(filename, encoding="utf-8"):
        with open(filename, 'r', encoding=encoding) as file:
            return file.read()

    @staticmethod
    def check_instance(filename):
        return os.path.exists(filename)
