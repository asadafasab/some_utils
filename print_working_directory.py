from pathlib import Path


class Pwd:
    def __init__(self):
        self.path = None

    def __call__(self):
        self.path = Path.cwd()
        print(self.path)


if __name__ == "__main__":
    pwd = Pwd()
    pwd()
