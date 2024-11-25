class Argument:
    def __init__(self, argument: str, bool: bool = False) -> None:
        self.argument = argument
        self.bool = bool


class CliParser:
    def __init__(self, arguments: list[Argument]) -> None:
        self.arguments = arguments

    def parse(self, argv: list[str]) -> None:
        for arg in argv:
            for argument in self.arguments:
                if arg == argument.argument:
                    argument.bool = True

    def check(self, arg: str) -> bool:
        for argument in self.arguments:
            if argument.argument == arg:
                return argument.bool
        return False
