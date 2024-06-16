# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lifebloom import Lifebloom, AsyncLifebloom

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCompletions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_action_steps(self, client: Lifebloom) -> None:
        completion = client.completions.create_action_steps()
        assert completion is None

    @parametrize
    def test_raw_response_create_action_steps(self, client: Lifebloom) -> None:
        response = client.completions.with_raw_response.create_action_steps()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        completion = response.parse()
        assert completion is None

    @parametrize
    def test_streaming_response_create_action_steps(self, client: Lifebloom) -> None:
        with client.completions.with_streaming_response.create_action_steps() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            completion = response.parse()
            assert completion is None

        assert cast(Any, response.is_closed) is True


class TestAsyncCompletions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create_action_steps(self, async_client: AsyncLifebloom) -> None:
        completion = await async_client.completions.create_action_steps()
        assert completion is None

    @parametrize
    async def test_raw_response_create_action_steps(self, async_client: AsyncLifebloom) -> None:
        response = await async_client.completions.with_raw_response.create_action_steps()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        completion = await response.parse()
        assert completion is None

    @parametrize
    async def test_streaming_response_create_action_steps(self, async_client: AsyncLifebloom) -> None:
        async with async_client.completions.with_streaming_response.create_action_steps() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            completion = await response.parse()
            assert completion is None

        assert cast(Any, response.is_closed) is True
