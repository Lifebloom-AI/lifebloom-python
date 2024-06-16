# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lifebloom import Lifebloom, AsyncLifebloom

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestThread:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Lifebloom) -> None:
        thread = client.thread.create()
        assert thread is None

    @parametrize
    def test_raw_response_create(self, client: Lifebloom) -> None:
        response = client.thread.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert thread is None

    @parametrize
    def test_streaming_response_create(self, client: Lifebloom) -> None:
        with client.thread.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert thread is None

        assert cast(Any, response.is_closed) is True


class TestAsyncThread:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncLifebloom) -> None:
        thread = await async_client.thread.create()
        assert thread is None

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncLifebloom) -> None:
        response = await async_client.thread.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert thread is None

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncLifebloom) -> None:
        async with async_client.thread.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert thread is None

        assert cast(Any, response.is_closed) is True
