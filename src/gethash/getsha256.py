from ._script import gethashcli, script_main


@gethashcli('SHA256')
def main(check, files, **kwargs):
    import hashlib
    script_main(hashlib.sha256(), '.sha256', check, files, **kwargs)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
