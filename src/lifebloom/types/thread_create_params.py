# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ThreadCreateParams"]


class ThreadCreateParams(TypedDict, total=False):
    thread_input: Required[object]
    """The current thread_state for this thread"""
