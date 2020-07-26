from ._script import gethashcli, script_main


@gethashcli('SHA1')
def main(check, files, **kwargs):
    import hashlib
    script_main(hashlib.sha1(), '.sha1', check, files, **kwargs)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
