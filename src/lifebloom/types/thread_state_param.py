# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ThreadStateParam", "ActionsContext", "ThreadHistory"]


class ActionsContext(TypedDict, total=False):
    action_name: Annotated[str, PropertyInfo(alias="actionName")]


class ThreadHistory(TypedDict, total=False):
    is_exit: Annotated[bool, PropertyInfo(alias="isExit")]

    next_stage_index: Annotated[int, PropertyInfo(alias="nextStageIndex")]

    stage_input: Annotated[object, PropertyInfo(alias="stageInput")]

    stage_name: Annotated[str, PropertyInfo(alias="stageName")]

    stage_output: Annotated[object, PropertyInfo(alias="stageOutput")]


class ThreadStateParam(TypedDict, total=False):
    actions_context: Annotated[Iterable[ActionsContext], PropertyInfo(alias="actionsContext")]

    mode: Literal["speed", "precision", "training"]
    """Mode to run thread completion"""

    next_stage_index: Annotated[int, PropertyInfo(alias="nextStageIndex")]

    original_thread_input: Annotated[object, PropertyInfo(alias="originalThreadInput")]

    persona: object

    thread_history: Annotated[Iterable[ThreadHistory], PropertyInfo(alias="threadHistory")]

    thread_id: Annotated[str, PropertyInfo(alias="threadId")]

    workflow_name: Annotated[str, PropertyInfo(alias="workflowName")]
