from pynput.keyboard import Key, Listener, Controller
from rich.console import Console
from rich.table import Table


class PRBT_Table():
    def __init__(self, terminal: Console, name: str, header: list, content: list) -> None:
        self.terminal = terminal
        self.name: str = name
        self.header: list = header
        self.lines: list = content
        self.table: Table = self._build()

    def build(self) -> None:
        self.table = self._build()

    def _build(self) -> Table:
        table = Table(title=self.name)
        for column in self.header:
            table.add_column(**column)
        for line in self.lines:
            table.add_row(*line)
        return table

    def render(self) -> None:
        self.terminal.clear()
        self.terminal.print(self.table)

class PRBT_iTable(PRBT_Table):
    def __init__(self, terminal: Console, name: str, header: list, content: list, keyboard: Controller) -> None:
        super().__init__(terminal, name, header, content)
        self.index = 0
        self.keyboard = keyboard

    
    def next(self) -> None:
        self.index = (self.index + 1) % len(content)
    
    def previous(self) -> None:
        if self.index == 0:
            self.index == len(content) - 1
        else:
            self.index -= 1

    def render(self) -> None:
        self.terminal.clear()
        for index, row in enumerate(self.table.rows):
            if index == self.index:
                row.style = "bold"
            else:
                row.style = None
        self.terminal.print(self.table)
    
    def on_press(self, key: Key):
        if key == Key.esc or key.char.lower() in ['q']:
            return False
        elif key == Key.tab:
            if self.keyboard.shift_pressed:
                self.previous()
            else:
                self.next()


def tests():
    def test_1():
        console = Console()
        name = "Star Wars Movies"
        header = [
            {"header":"Released", "justify":"right", "style":"cyan", "no_wrap":True},
            {"header":"Title", "style":"magenta"},
            {"header":"Box Office", "justify":"right", "style":"green"},
        ]
        content = [
            ["Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690"],
            ["May 25, 2018", "Solo: A Star Wars Story", "$393,151,347"],
            ["Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889"],
            ["Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889"],
        ]

        table = PRBT_Table(terminal=console, name=name, header=header, content=content)
        table.render()
    
    def test2():
        console = Console()
        name = "Star Wars Movies"
        header = [
            {"header":"Released", "justify":"right", "style":"cyan", "no_wrap":True},
            {"header":"Title", "style":"magenta"},
            {"header":"Box Office", "justify":"right", "style":"green"},
        ]
        content = [
            ["Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690"],
            ["May 25, 2018", "Solo: A Star Wars Story", "$393,151,347"],
            ["Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889"],
            ["Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889"],
        ]

        table = PRBT_iTable(terminal=console, name=name, header=header, content=content)
        for x in range(4):
            table.render()
            console.input("Waiting for input")
            table.next()



if __name__ == "__main__":
    console = Console()
    keyboard = Controller()
    name = "Star Wars Movies"
    header = [
        {"header":"Released", "justify":"right", "style":"cyan", "no_wrap":True},
        {"header":"Title", "style":"magenta"},
        {"header":"Box Office", "justify":"right", "style":"green"},
    ]
    content = [
        ["Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690"],
        ["May 25, 2018", "Solo: A Star Wars Story", "$393,151,347"],
        ["Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889"],
        ["Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889"],
    ]

    table = PRBT_iTable(terminal=console, name=name, header=header, content=content, keyboard=keyboard)