from ._script import gethashcli, script_main


@gethashcli('MD5')
def main(check, files, **kwargs):
    import hashlib
    script_main(main, hashlib.md5(), '.md5', check, files, **kwargs)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
