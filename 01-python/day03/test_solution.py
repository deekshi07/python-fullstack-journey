"""Automated unit test suite for Day 03: Functions, Scopes & Closures."""

from __future__ import annotations

import pytest

from .solution import (
    build_api_url,
    configure_service,
    create_rate_limiter,
    execute_with_fallback,
)


class TestBuildApiUrl:
    def test_standard_url_generation(self) -> None:
        url = build_api_url("api.example.com", "users", page=1, limit=20)
        assert url == "https://api.example.com/users?page=1&limit=20"

    def test_variadic_path_segments(self) -> None:
        url = build_api_url("api.example.com", "v1", "organizations", "123", "members")
        assert url == "https://api.example.com/v1/organizations/123/members"

    def test_http_scheme_override(self) -> None:
        url = build_api_url("localhost:8000", "health", https=False)
        assert url == "http://localhost:8000/health"

    def test_positional_only_constraint(self) -> None:
        """Calling positional-only arguments via keyword must fail."""
        with pytest.raises(TypeError):
            # 'base_url' is before '/', so it cannot be passed as a keyword
            build_api_url(base_url="api.example.com", endpoint="users")  # type: ignore[call-arg]

    def test_keyword_only_constraint(self) -> None:
        """Calling keyword-only arguments positionally must fail."""
        # Valid keyword call:
        assert configure_service(timeout=60, retry_count=5) == {"timeout": 60, "retry_count": 5}

        # Calling positionally MUST raise TypeError
        with pytest.raises(TypeError):
            configure_service(60, 5)  # type: ignore[call-arg]


class TestRateLimiterClosure:
    def test_rate_limiter_allows_under_threshold(self) -> None:
        limiter = create_rate_limiter(max_requests=2)
        assert limiter() is True
        assert limiter() is True
        assert limiter() is False  # Limit reached

    def test_separate_rate_limiters_have_independent_state(self) -> None:
        """Verifies that separate closure instances do not share state."""
        limiter_a = create_rate_limiter(max_requests=1)
        limiter_b = create_rate_limiter(max_requests=2)

        assert limiter_a() is True
        assert limiter_a() is False  # A is exhausted

        # B should still have its full budget
        assert limiter_b() is True
        assert limiter_b() is True
        assert limiter_b() is False

    def test_invalid_limit_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            create_rate_limiter(max_requests=0)


class TestExecuteWithFallback:
    def test_primary_succeeds(self) -> None:
        def primary(x: int, multiplier: int = 2) -> int:
            return x * multiplier

        def fallback(x: int, multiplier: int = 2) -> int:
            return 0

        result = execute_with_fallback(primary, fallback, 10, multiplier=3)
        assert result == 30

    def test_fallback_triggers_on_exception(self) -> None:
        def failing_primary(x: int) -> int:
            raise ConnectionError("Service unavailable")

        def fallback(x: int) -> int:
            return x * 100

        result = execute_with_fallback(failing_primary, fallback, 5)
        assert result == 500
