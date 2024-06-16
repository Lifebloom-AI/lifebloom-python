# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import thread_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
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
from ..types.api_response_param import APIResponseParam

__all__ = ["ThreadResource", "AsyncThreadResource"]


class ThreadResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ThreadResourceWithRawResponse:
        return ThreadResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ThreadResourceWithStreamingResponse:
        return ThreadResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        thread_state: APIResponseParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Take a thread_state and return next action steps

        Args:
          thread_state: The current thread_state for this thread

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/thread",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"thread_state": thread_state}, thread_create_params.ThreadCreateParams),
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

    async def create(
        self,
        *,
        thread_state: APIResponseParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Take a thread_state and return next action steps

        Args:
          thread_state: The current thread_state for this thread

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/thread",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"thread_state": thread_state}, thread_create_params.ThreadCreateParams
                ),
            ),
            cast_to=NoneType,
        )


class ThreadResourceWithRawResponse:
    def __init__(self, thread: ThreadResource) -> None:
        self._thread = thread

        self.create = to_raw_response_wrapper(
            thread.create,
        )


class AsyncThreadResourceWithRawResponse:
    def __init__(self, thread: AsyncThreadResource) -> None:
        self._thread = thread

        self.create = async_to_raw_response_wrapper(
            thread.create,
        )


class ThreadResourceWithStreamingResponse:
    def __init__(self, thread: ThreadResource) -> None:
        self._thread = thread

        self.create = to_streamed_response_wrapper(
            thread.create,
        )


class AsyncThreadResourceWithStreamingResponse:
    def __init__(self, thread: AsyncThreadResource) -> None:
        self._thread = thread

        self.create = async_to_streamed_response_wrapper(
            thread.create,
        )
