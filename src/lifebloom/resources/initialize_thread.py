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

__all__ = ["InitializeThreadResource", "AsyncInitializeThreadResource"]


class InitializeThreadResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> InitializeThreadResourceWithRawResponse:
        return InitializeThreadResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InitializeThreadResourceWithStreamingResponse:
        return InitializeThreadResourceWithStreamingResponse(self)

    def create(
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


class AsyncInitializeThreadResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncInitializeThreadResourceWithRawResponse:
        return AsyncInitializeThreadResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInitializeThreadResourceWithStreamingResponse:
        return AsyncInitializeThreadResourceWithStreamingResponse(self)

    async def create(
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


class InitializeThreadResourceWithRawResponse:
    def __init__(self, initialize_thread: InitializeThreadResource) -> None:
        self._initialize_thread = initialize_thread

        self.create = to_raw_response_wrapper(
            initialize_thread.create,
        )


class AsyncInitializeThreadResourceWithRawResponse:
    def __init__(self, initialize_thread: AsyncInitializeThreadResource) -> None:
        self._initialize_thread = initialize_thread

        self.create = async_to_raw_response_wrapper(
            initialize_thread.create,
        )


class InitializeThreadResourceWithStreamingResponse:
    def __init__(self, initialize_thread: InitializeThreadResource) -> None:
        self._initialize_thread = initialize_thread

        self.create = to_streamed_response_wrapper(
            initialize_thread.create,
        )


class AsyncInitializeThreadResourceWithStreamingResponse:
    def __init__(self, initialize_thread: AsyncInitializeThreadResource) -> None:
        self._initialize_thread = initialize_thread

        self.create = async_to_streamed_response_wrapper(
            initialize_thread.create,
        )
