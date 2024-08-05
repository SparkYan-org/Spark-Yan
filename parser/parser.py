import yaml
import GameObject

try:
    from yaml import Cloader as Loader
except ImportError:
    from yaml import Loader

import os.path as path
import dill


class Parser:
    def __init__(self, path):
        self.path = path
        self.game = GameObject.Game()

    def load_manifest(self):
        f = open(path.join(self.path, "manifest.yml"))
        file = yaml.load(f.read(), Loader=Loader)
        self.game.manifest = GameObject.GameConfig(file, self.path)

    def load_roles(self):
        f = open(path.join(self.path, self.game.manifest.src, "roles.yml"))
        file = yaml.load(f.read(), Loader=Loader)["roles"]

        for item in file:
            self.game.roles.append(GameObject.GameRole(item))

    def load_plot(self):
        f = open(self.game.manifest.endpoint)
        file = yaml.load(f.read(), Loader=Loader)
        self.game.plot = GameObject.GamePlot(file)

    def parser(self):
        self.load_manifest()
        self.load_roles()
        self.load_plot()
        return self.game


if __name__ == "__main__":
    parser = Parser("test")
    game = parser.parser()
    print(game)
    dill.dump(game, open("test.syp", "wb"))
