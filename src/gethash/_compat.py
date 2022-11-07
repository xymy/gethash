import sys

if sys.version_info[:2] < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points  # noqa
