# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import (
    make_request_options,
)

__all__ = ["ThreadResource", "AsyncThreadResource"]


class ThreadResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ThreadResourceWithRawResponse:
        return ThreadResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ThreadResourceWithStreamingResponse:
        return ThreadResourceWithStreamingResponse(self)

    def completion(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Take a thread_state and return next action steps"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/thread",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def initialize_thread(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Initialize thread and recieve an empty thread state object"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/initializeThread",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncThreadResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncThreadResourceWithRawResponse:
        return AsyncThreadResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncThreadResourceWithStreamingResponse:
        return AsyncThreadResourceWithStreamingResponse(self)

    async def completion(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Take a thread_state and return next action steps"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/thread",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def initialize_thread(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Initialize thread and recieve an empty thread state object"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/initializeThread",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class ThreadResourceWithRawResponse:
    def __init__(self, thread: ThreadResource) -> None:
        self._thread = thread

        self.completion = to_raw_response_wrapper(
            thread.completion,
        )
        self.initialize_thread = to_raw_response_wrapper(
            thread.initialize_thread,
        )


class AsyncThreadResourceWithRawResponse:
    def __init__(self, thread: AsyncThreadResource) -> None:
        self._thread = thread

        self.completion = async_to_raw_response_wrapper(
            thread.completion,
        )
        self.initialize_thread = async_to_raw_response_wrapper(
            thread.initialize_thread,
        )


class ThreadResourceWithStreamingResponse:
    def __init__(self, thread: ThreadResource) -> None:
        self._thread = thread

        self.completion = to_streamed_response_wrapper(
            thread.completion,
        )
        self.initialize_thread = to_streamed_response_wrapper(
            thread.initialize_thread,
        )


class AsyncThreadResourceWithStreamingResponse:
    def __init__(self, thread: AsyncThreadResource) -> None:
        self._thread = thread

        self.completion = async_to_streamed_response_wrapper(
            thread.completion,
        )
        self.initialize_thread = async_to_streamed_response_wrapper(
            thread.initialize_thread,
        )
