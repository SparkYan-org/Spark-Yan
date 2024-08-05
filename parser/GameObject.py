# pylint:disable=W0707
from os import path


class GameConfig:
    def __init__(self, file, base_dir):
        self.file = file
        try:
            self.name = file["name"]
            self.version = file.get("version", "1.0.0")
            self.author = file["author"]

            self.src = file.get("src", ".")
            self.endpoint = path.join(
                base_dir, self.src, file.get("endpoint", "start") + ".yml"
            )

            f = file.get("files", {})
            self.files = {
                "audio": f.get("audio", "assets/audio"),
                "images": f.get("images", "assets/images"),
            }

            self.env = file.get("env", [])

            self.android = file.get("android", {})
            self.windows = file.get("windows", {})
            self.macos = file.get("macos", {})

        except KeyError as e:
            raise KeyError("无法获取到清单文件中的：" + e.args[0])

    def __str__(self):
        return str(self.file)

    def __repr__(self):
        return str(self.file)


class GameRole:
    def __init__(self, item):
        self.name = item.get("name")
        self.id = item.get("id", self.name)
        self.base_dir = item.get("base_dir", self.name)

    def __eq__(self, other):
        if isinstance(other, GameRole):
            if self.id == other.id:
                return True
            else:
                return False
        return False

    def __str__(self):
        return f"GameRole({self.name})"

    def __repr__(self):
        return f"GameRole({self.name})"


class GameDialog:
    def __init__(self, item):
        self.role = item["role"]

        if "msg" in item:
            self.choice = False
            self.msg = item["msg"]

        elif "choices" in item:
            self.choice = True
            self.choices = []
            for option in item["choices"]:
                option["role"] = self.role
                self.choices.append(GameDialog(option))

        else:
            raise KeyError("不正确的对话格式")

    def __str__(self):
        if self.choice:
            return f"GamePlot({self.role}, {self.choices})"
        else:
            return f"GamePlot({self.role} {self.msg})"

    def __repr__(self):
        return self.__str__()


class GamePlot:
    def __init__(self, file):
        self.file = file
        self.scenes = []
        self.content = []
        self.endpoint = None
        self.parser()

    def parser(self):
        for dialog in self.file["content"]:

            self.content.append(GameDialog(dialog))

    def __str__(self):
        return str(self.content)


class Game:
    def __init__(self):
        self.manifest: GameConfig = None
        self.roles: list[GameRole] = []
        self.plot: GamePlot = None

    def __str__(self):
        return f"{self.manifest}\n{self.roles}\n{self.plot}"
