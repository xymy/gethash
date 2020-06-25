import hashlib

import click

from ._core import script_main


@click.command()
@click.option('-c', '--check', is_flag=True,
              help='read SHA1 from the FILES and check them.')
@click.argument('files', nargs=-1)
def main(check, files):
    script_main(main, hashlib.sha1(), '.sha1', check, files)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
