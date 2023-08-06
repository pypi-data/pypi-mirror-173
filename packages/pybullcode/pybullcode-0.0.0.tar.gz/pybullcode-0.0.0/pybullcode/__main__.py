from bullcode.cmp import Compiler

import sys
import click

@click.group()
@click.version_option("1.0.0")
def main():
    pass

@main.command()
@click.argument('keyword', required=False)
def run(**kwargs):
    file = kwargs["keyword"]
    comp = Compiler(config="__main__")
    comp.run(code=open(file).read())

if __name__ == '__main__':
    args = sys.argv
    main()
