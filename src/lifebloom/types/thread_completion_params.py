# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .thread_state_param import ThreadStateParam

__all__ = ["ThreadCompletionParams"]


class ThreadCompletionParams(TypedDict, total=False):
    thread_state: Required[ThreadStateParam]
    """The current thread_state for this thread"""
