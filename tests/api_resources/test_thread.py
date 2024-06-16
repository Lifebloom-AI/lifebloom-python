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
        thread = client.thread.create(
            thread_input={},
        )
        assert thread is None

    @parametrize
    def test_raw_response_create(self, client: Lifebloom) -> None:
        response = client.thread.with_raw_response.create(
            thread_input={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert thread is None

    @parametrize
    def test_streaming_response_create(self, client: Lifebloom) -> None:
        with client.thread.with_streaming_response.create(
            thread_input={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert thread is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_completion(self, client: Lifebloom) -> None:
        thread = client.thread.completion(
            thread_state={},
        )
        assert thread is None

    @parametrize
    def test_method_completion_with_all_params(self, client: Lifebloom) -> None:
        thread = client.thread.completion(
            thread_state={
                "thread_id": "3e429065-3a88-4b30-bb82-ef6c11f134f3",
                "original_thread_input": {},
                "mode": "precision",
                "persona": {},
                "next_stage_index": 0,
                "workflow_name": "security_finding_investigation",
                "thread_history": [
                    {
                        "stage_name": "security_finding_recursive_investigation",
                        "stage_input": {},
                        "stage_output": {},
                        "is_exit": True,
                        "next_stage_index": 0,
                    },
                    {
                        "stage_name": "security_finding_recursive_investigation",
                        "stage_input": {},
                        "stage_output": {},
                        "is_exit": True,
                        "next_stage_index": 0,
                    },
                    {
                        "stage_name": "security_finding_recursive_investigation",
                        "stage_input": {},
                        "stage_output": {},
                        "is_exit": True,
                        "next_stage_index": 0,
                    },
                ],
                "actions_context": [{"action_name": "string"}, {"action_name": "string"}, {"action_name": "string"}],
            },
        )
        assert thread is None

    @parametrize
    def test_raw_response_completion(self, client: Lifebloom) -> None:
        response = client.thread.with_raw_response.completion(
            thread_state={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert thread is None

    @parametrize
    def test_streaming_response_completion(self, client: Lifebloom) -> None:
        with client.thread.with_streaming_response.completion(
            thread_state={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert thread is None

        assert cast(Any, response.is_closed) is True


class TestAsyncThread:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncLifebloom) -> None:
        thread = await async_client.thread.create(
            thread_input={},
        )
        assert thread is None

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncLifebloom) -> None:
        response = await async_client.thread.with_raw_response.create(
            thread_input={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert thread is None

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncLifebloom) -> None:
        async with async_client.thread.with_streaming_response.create(
            thread_input={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert thread is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_completion(self, async_client: AsyncLifebloom) -> None:
        thread = await async_client.thread.completion(
            thread_state={},
        )
        assert thread is None

    @parametrize
    async def test_method_completion_with_all_params(self, async_client: AsyncLifebloom) -> None:
        thread = await async_client.thread.completion(
            thread_state={
                "thread_id": "3e429065-3a88-4b30-bb82-ef6c11f134f3",
                "original_thread_input": {},
                "mode": "precision",
                "persona": {},
                "next_stage_index": 0,
                "workflow_name": "security_finding_investigation",
                "thread_history": [
                    {
                        "stage_name": "security_finding_recursive_investigation",
                        "stage_input": {},
                        "stage_output": {},
                        "is_exit": True,
                        "next_stage_index": 0,
                    },
                    {
                        "stage_name": "security_finding_recursive_investigation",
                        "stage_input": {},
                        "stage_output": {},
                        "is_exit": True,
                        "next_stage_index": 0,
                    },
                    {
                        "stage_name": "security_finding_recursive_investigation",
                        "stage_input": {},
                        "stage_output": {},
                        "is_exit": True,
                        "next_stage_index": 0,
                    },
                ],
                "actions_context": [{"action_name": "string"}, {"action_name": "string"}, {"action_name": "string"}],
            },
        )
        assert thread is None

    @parametrize
    async def test_raw_response_completion(self, async_client: AsyncLifebloom) -> None:
        response = await async_client.thread.with_raw_response.completion(
            thread_state={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert thread is None

    @parametrize
    async def test_streaming_response_completion(self, async_client: AsyncLifebloom) -> None:
        async with async_client.thread.with_streaming_response.completion(
            thread_state={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert thread is None

        assert cast(Any, response.is_closed) is True
