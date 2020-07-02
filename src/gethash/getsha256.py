import click

from ._script import script_main


@click.command()
@click.option('-c', '--check', is_flag=True,
              help='read SHA256 from the FILES and check them.')
@click.option('--no-stdout', is_flag=True,
              help='Do not output to stdout.')
@click.option('--no-stderr', is_flag=True,
              help='Do not output to stderr.')
@click.option('--no-glob', is_flag=True,
              help='Do not resolve glob patterns.')
@click.version_option()
@click.argument('files', nargs=-1)
def main(check, files, **kwargs):
    import hashlib
    script_main(main, hashlib.sha256(), '.sha256', check, files, **kwargs)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
