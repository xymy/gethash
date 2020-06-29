import hashlib

import click

from ._core import script_main


@click.command()
@click.option('-c', '--check', is_flag=True,
              help='read SHA1 from the FILES and check them.')
@click.option('--no-stdout', is_flag=True,
              help='Do not output to stdout.')
@click.version_option()
@click.argument('files', nargs=-1)
def main(check, files, **kwargs):
    script_main(main, hashlib.sha1(), '.sha1', check, files, **kwargs)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
