import os
if os.name == "nt":
    from windows import scanner
elif os.name == "posix":
    from unix import scanner


class localizator:
    def __init__ (self):
        self.Scanner = scanner()


if __name__ == "__main__":
    locate = localizator()