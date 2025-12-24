"""Top-level package for Django project apps.

This file makes `apps` a regular package so that unittest test
discovery can resolve package paths (avoids namespace package issues).
"""

__all__ = [
    "users",
    "business",
    "cashflow",
    "loans",
    "advice",
]
