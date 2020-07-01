import hashlib

import click

from ._script import script_main


@click.command()
@click.option('-c', '--check', is_flag=True,
              help='read MD5 from the FILES and check them.')
@click.option('--no-stdout', is_flag=True,
              help='Do not output to stdout.')
@click.option('--no-stderr', is_flag=True,
              help='Do not output to stderr.')
@click.version_option()
@click.argument('files', nargs=-1)
def main(check, files, **kwargs):
    script_main(main, hashlib.md5(), '.md5', check, files, **kwargs)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
