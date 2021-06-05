import sys
from typing import Any, Dict, Optional

import click


def _configure_context_settings(attrs: Dict[str, Any]) -> None:
    context_settings = attrs.pop("context_settings", {})
    context_settings.setdefault("max_content_width", 120)
    context_settings.setdefault("help_option_names", ["-h", "--help"])
    attrs["context_settings"] = context_settings


class Command(click.Command):
    def __init__(self, name: Optional[str], **attrs: Any) -> None:
        _configure_context_settings(attrs)
        super().__init__(name, **attrs)

    def main(self, args=None, **kwargs):
        if args is None:
            args = sys.argv[1:]
        return super().main(args, **kwargs)


class MultiCommand(click.MultiCommand):
    def __init__(self, name: Optional[str], **attrs: Any) -> None:
        _configure_context_settings(attrs)
        super().__init__(name, **attrs)

    def main(self, args=None, **kwargs):
        if args is None:
            args = sys.argv[1:]
        return super().main(args, **kwargs)


class Group(click.Group):
    def __init__(self, name: Optional[str], **attrs: Any) -> None:
        _configure_context_settings(attrs)
        super().__init__(name, **attrs)

    def main(self, args=None, **kwargs):
        if args is None:
            args = sys.argv[1:]
        return super().main(args, **kwargs)


class CommandCollection(click.CommandCollection):
    def __init__(self, name: Optional[str], **attrs: Any) -> None:
        _configure_context_settings(attrs)
        super().__init__(name, **attrs)

    def main(self, args=None, **kwargs):
        if args is None:
            args = sys.argv[1:]
        return super().main(args, **kwargs)
