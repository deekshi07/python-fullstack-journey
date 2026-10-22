"""Day 02: Comprehensions, Generator Expressions, and Memory Optimization.

Demonstrates production standards:
1. List comprehension with safe filtering and normalization.
2. Dictionary comprehension for O(1) index lookups.
3. Set comprehension for deduplication.
4. Generator expressions for streaming data with O(1) memory footprint.
"""

from __future__ import annotations

import sys
from collections.abc import Iterator
from typing import Any


def filter_active_user_emails(users: list[dict[str, Any]]) -> list[str]:
    """Extracts and normalizes emails for active users using list comprehension.

    Args:
        users: A list of user dictionaries from a database or API response.

    Returns:
        A list of clean, lowercase emails for active users only.
    """
    return [
        str(u["email"]).strip().lower()
        for u in users
        if u.get("is_active") is True and u.get("email")
    ]


def build_user_id_lookup(users: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    """Builds an O(1) ID-to-User lookup dictionary using dict comprehension.

    Args:
        users: A list of user dictionaries containing an 'id' key.

    Returns:
        Mapping of user ID to the full user dictionary.
    """
    return {int(u["id"]): u for u in users if "id" in u and u["id"] is not None}


def extract_unique_roles(users: list[dict[str, Any]]) -> set[str]:
    """Extracts unique user roles in lowercase using set comprehension.

    Args:
        users: A list of user dictionaries.

    Returns:
        A set of unique role names.
    """
    return {
        str(u["role"]).strip().lower() for u in users if u.get("role") and str(u["role"]).strip()
    }


def stream_even_squares(limit: int) -> Iterator[int]:
    """Generates squares of even numbers up to limit using a generator expression.

    Memory Complexity: O(1) regardless of whether limit is 10 or 10,000,000.
    """
    return (x * x for x in range(limit) if x % 2 == 0)


def compare_memory_footprint(count: int) -> tuple[int, int]:
    """Compares the exact byte size of a list comprehension vs generator expression in RAM.

    Args:
        count: Number of elements to evaluate.

    Returns:
        Tuple of (list_bytes, generator_bytes).
    """
    list_version = [x for x in range(count)]
    gen_version = (x for x in range(count))

    return (sys.getsizeof(list_version), sys.getsizeof(gen_version))
