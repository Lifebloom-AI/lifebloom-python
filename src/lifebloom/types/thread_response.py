# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .thread_state import ThreadState

__all__ = ["ThreadResponse", "Action"]


class Action(BaseModel):
    action_name: Optional[str] = FieldInfo(alias="actionName", default=None)


class ThreadResponse(BaseModel):
    actions: Optional[List[Action]] = None

    thread_state: Optional[ThreadState] = None
