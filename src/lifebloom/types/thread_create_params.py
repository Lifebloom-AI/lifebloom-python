# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .api_response_param import APIResponseParam

__all__ = ["ThreadCreateParams"]


class ThreadCreateParams(TypedDict, total=False):
    thread_state: Required[APIResponseParam]
    """The current thread_state for this thread"""
