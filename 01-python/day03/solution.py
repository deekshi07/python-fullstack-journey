"""Day 03: Functions, Parameter Ordering, Scopes, and Closures.

Production Implementations:
1. build_api_url: Demonstrates positional-only (/), variadic args (*args),
   keyword-only (*), and variadic keyword args (**kwargs).
2. create_rate_limiter: Demonstrates closures and the `nonlocal` keyword to
   encapsulate private state.
3. execute_with_fallback: Demonstrates first-class functions and argument unpacking.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any
from urllib.parse import urlencode


def build_api_url(
    base_url: str,
    endpoint: str,
    /,
    *path_segments: str,
    https: bool = True,
    **query_params: Any,
) -> str:
    """Constructs a normalized API URL with strict parameter semantics.

    - base_url & endpoint are POSITIONAL-ONLY (before `/`).
    - *path_segments captures any extra sub-paths as a tuple.
    - https is KEYWORD-ONLY (after `*`).
    - **query_params captures query parameters as a dictionary.
    """
    scheme = "https" if https else "http"
    clean_base = base_url.replace("http://", "").replace("https://", "").strip("/")
    clean_endpoint = endpoint.strip("/")

    # Combine all path components cleanly
    parts = [clean_base, clean_endpoint]
    for seg in path_segments:
        seg_str = str(seg).strip("/")
        if seg_str:
            parts.append(seg_str)

    url = f"{scheme}://{'/'.join(parts)}"

    # Append query params if provided
    if query_params:
        clean_params = {k: v for k, v in query_params.items() if v is not None}
        if clean_params:
            url = f"{url}?{urlencode(clean_params)}"

    return url


def configure_service(*, timeout: int = 30, retry_count: int = 3) -> dict[str, int]:
    """Pure keyword-only configuration function.

    The bare `*` syntax forces ALL parameters after it to be passed by keyword.
    """
    return {"timeout": timeout, "retry_count": retry_count}


def create_rate_limiter(max_requests: int) -> Callable[[], bool]:
    """Creates a rate limiter closure that tracks internal state using `nonlocal`.

    Args:
        max_requests: Maximum allowed calls before throttling.

    Returns:
        A callable function that returns True if allowed, or False if throttled.
    """
    if max_requests <= 0:
        raise ValueError("max_requests must be greater than 0")

    current_count = 0  # Enclosing scope variable

    def check_and_increment() -> bool:
        nonlocal current_count  # Modifies the enclosing variable
        if current_count < max_requests:
            current_count += 1
            return True
        return False

    return check_and_increment


def execute_with_fallback(
    primary_fn: Callable[..., Any],
    fallback_fn: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Executes a primary function; falls back to an alternative on failure.

    Demonstrates first-class functions and argument unpacking (*args, **kwargs).
    """
    try:
        # Unpacking positional and keyword arguments dynamically
        return primary_fn(*args, **kwargs)
    except Exception:
        return fallback_fn(*args, **kwargs)
