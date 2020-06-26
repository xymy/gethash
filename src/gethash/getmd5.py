import hashlib

import click

from ._core import script_main


@click.command()
@click.option('-c', '--check', is_flag=True,
              help='read MD5 from the FILES and check them.')
@click.version_option()
@click.argument('files', nargs=-1)
def main(check, files):
    script_main(main, hashlib.md5(), '.md5', check, files)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
