# pylint:disable=W4901
import click
from parser import Parser
from info import Engine

import render


@click.command()
@click.argument("path")
@click.option(
    "-d",
    "--dist",
    default="dist",
)
def cli(path, dist):
    GameParser = Parser(path)

    game = GameParser.parser()

    render.render(game, Engine, dist)
