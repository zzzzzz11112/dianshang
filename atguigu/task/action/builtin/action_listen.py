from __future__ import annotations

# atguigu/task/action/builtin/action_listen.py
import asyncio
from typing import Any

from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult


class ActionListen(Action):
    """
    什么都不做，返回空的ActionResult
    """
    name = "action_listen"

    async def run(self, state: DialogueState, action_kwargs: dict[str, Any]) -> ActionResult:
        print("action_listen")
        return ActionResult()
