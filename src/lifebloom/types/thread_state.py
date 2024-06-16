# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ThreadState", "ActionsContext", "ThreadHistory"]


class ActionsContext(BaseModel):
    action_name: Optional[str] = FieldInfo(alias="actionName", default=None)


class ThreadHistory(BaseModel):
    is_exit: Optional[bool] = FieldInfo(alias="isExit", default=None)

    next_stage_index: Optional[int] = FieldInfo(alias="nextStageIndex", default=None)

    stage_input: Optional[object] = FieldInfo(alias="stageInput", default=None)

    stage_name: Optional[str] = FieldInfo(alias="stageName", default=None)

    stage_output: Optional[object] = FieldInfo(alias="stageOutput", default=None)


class ThreadState(BaseModel):
    actions_context: Optional[List[ActionsContext]] = FieldInfo(alias="actionsContext", default=None)

    mode: Optional[Literal["speed", "precision", "training"]] = None
    """Mode to run thread completion"""

    next_stage_index: Optional[int] = FieldInfo(alias="nextStageIndex", default=None)

    original_thread_input: Optional[object] = FieldInfo(alias="originalThreadInput", default=None)

    persona: Optional[object] = None

    thread_history: Optional[List[ThreadHistory]] = FieldInfo(alias="threadHistory", default=None)

    thread_id: Optional[str] = FieldInfo(alias="threadId", default=None)

    workflow_name: Optional[str] = FieldInfo(alias="workflowName", default=None)
