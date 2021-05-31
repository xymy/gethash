import sys

import click


class Command(click.Command):
    def __init__(self, name, context_settings=None, **kwargs):
        if context_settings is None:
            context_settings = {}
        context_settings.setdefault("max_content_width", 120)
        context_settings.setdefault("help_option_names", ["-h", "--help"])
        super().__init__(name, context_settings=context_settings, **kwargs)

    def main(self, args=None, **kwargs):
        if args is None:
            args = sys.argv[1:]
        return super().main(args, **kwargs)


class MultiCommand(click.MultiCommand):
    def __init__(self, name, context_settings=None, **kwargs):
        if context_settings is None:
            context_settings = {}
        context_settings.setdefault("max_content_width", 120)
        context_settings.setdefault("help_option_names", ["-h", "--help"])
        super().__init__(name, context_settings=context_settings, **kwargs)

    def main(self, args=None, **kwargs):
        if args is None:
            args = sys.argv[1:]
        return super().main(args, **kwargs)


class Group(click.Group):
    def __init__(self, name, context_settings=None, **kwargs):
        if context_settings is None:
            context_settings = {}
        context_settings.setdefault("max_content_width", 120)
        context_settings.setdefault("help_option_names", ["-h", "--help"])
        super().__init__(name, context_settings=context_settings, **kwargs)

    def main(self, args=None, **kwargs):
        if args is None:
            args = sys.argv[1:]
        return super().main(args, **kwargs)


class CommandCollection(click.CommandCollection):
    def __init__(self, name, context_settings=None, **kwargs):
        if context_settings is None:
            context_settings = {}
        context_settings.setdefault("max_content_width", 120)
        context_settings.setdefault("help_option_names", ["-h", "--help"])
        super().__init__(name, context_settings=context_settings, **kwargs)

    def main(self, args=None, **kwargs):
        if args is None:
            args = sys.argv[1:]
        return super().main(args, **kwargs)
