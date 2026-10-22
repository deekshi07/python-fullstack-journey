"""Automated unit test suite for Day 02: Comprehensions and Generators."""

from __future__ import annotations

import types
from typing import Any

from .solution import (
    build_user_id_lookup,
    compare_memory_footprint,
    extract_unique_roles,
    filter_active_user_emails,
    stream_even_squares,
)


class TestComprehensions:
    def test_filter_active_user_emails(self) -> None:
        raw_users: list[dict[str, Any]] = [
            {"id": 1, "email": " Alice@Example.COM ", "is_active": True},
            {"id": 2, "email": "bob@example.com", "is_active": False},
            {"id": 3, "email": "charlie@company.org", "is_active": True},
            {"id": 4, "email": "", "is_active": True},  # Empty email edge case
            {"id": 5, "is_active": True},  # Missing email key
        ]

        result = filter_active_user_emails(raw_users)
        assert result == ["alice@example.com", "charlie@company.org"]

    def test_build_user_id_lookup(self) -> None:
        raw_users: list[dict[str, Any]] = [
            {"id": 101, "name": "Alice"},
            {"id": 102, "name": "Bob"},
            {"id": "103", "name": "Charlie"},  # String ID converted to int
        ]

        lookup = build_user_id_lookup(raw_users)
        assert 101 in lookup
        assert lookup[101]["name"] == "Alice"
        assert lookup[103]["name"] == "Charlie"

    def test_extract_unique_roles(self) -> None:
        raw_users: list[dict[str, Any]] = [
            {"name": "Alice", "role": "admin"},
            {"name": "Bob", "role": "ADMIN"},  # Case variation
            {"name": "Charlie", "role": "developer"},
            {"name": "Dave", "role": "  developer  "},
            {"name": "Eve", "role": ""},
        ]

        roles = extract_unique_roles(raw_users)
        assert roles == {"admin", "developer"}


class TestGeneratorAndMemory:
    def test_stream_even_squares_is_lazy(self) -> None:
        generator = stream_even_squares(10)
        assert isinstance(generator, types.GeneratorType)

        # First 3 even squares: 0*0=0, 2*2=4, 4*4=16
        assert next(generator) == 0
        assert next(generator) == 4
        assert next(generator) == 16

        # Consuming the remaining items
        remaining = list(generator)
        assert remaining == [36, 64]  # 6*6=36, 8*8=64

    def test_compare_memory_footprint(self) -> None:
        list_bytes, gen_bytes = compare_memory_footprint(100_000)

        # The list holding 100,000 items takes hundreds of kilobytes
        assert list_bytes > 500_000
        # The generator expression consumes less than 300 bytes
        assert gen_bytes < 300
