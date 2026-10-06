from .vb6 import VB6Parser


def default_parsers():
    """Parsers shipped with this version. Delphi and PL/SQL are on the roadmap."""
    return [VB6Parser()]


__all__ = ["VB6Parser", "default_parsers"]
