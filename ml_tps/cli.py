# -*- coding: utf-8 -*-

"""Console script for ml_tps."""
import sys
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@click.command()
def main(args=None):
    """Console script for ml_tps."""
    click.echo("Replace this message by putting your code into "
               "ml_tps.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


@click.command()
def e1_1():
    print("1.1")


@click.command()
def e1_2():
    print("1.2")


@click.command()
def e1_3():
    print("1.3")


cli.add_command(e1_1)
cli.add_command(e1_2)
cli.add_command(e1_3)

if __name__ == '__main__':
    cli()