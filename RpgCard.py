EQUIPMENT_COLOR = 'dimgray'


class RpgCard:
    count: int
    color: str
    title: str
    icon: str
    icon_back: str
    contents: list[str]

    def __init__(self):
        self.color = EQUIPMENT_COLOR
        self.count = 1
        self.title = ''
        self.icon = ''
        self.icon_back = ''
        self.contents = []

    def append_content(self, line: str):
        self.contents.append(line)

    def extend_content(self, lines: list):
        self.contents.extend(lines)
