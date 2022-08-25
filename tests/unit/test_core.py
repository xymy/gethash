from gethash.core import format_hash_line, parse_hash_line


def test_format_hash_line() -> None:
    result = format_hash_line("d41d8cd98f00b204e9800998ecf8427e", "foo.txt")
    assert result == "d41d8cd98f00b204e9800998ecf8427e *foo.txt\n"


def test_parse_hash_line() -> None:
    result = parse_hash_line("d41d8cd98f00b204e9800998ecf8427e *foo.txt\n")
    assert result == ("d41d8cd98f00b204e9800998ecf8427e", "foo.txt")
