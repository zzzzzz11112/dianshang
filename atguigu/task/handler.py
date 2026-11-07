from __future__ import annotations

# atguigu/task/handler.py

from atguigu.domain.messages import BotMessage
from atguigu.domain.state import DialogueState
from atguigu.task.action.runner import ActionRunner
from atguigu.task.command.models import Command
from atguigu.task.command.processor import CommandProcessor
from atguigu.task.flow.executor import FlowExecutor
from atguigu.task.flow.flows import FlowsList

class TaskHandler:

    def __init__(
            self,
            flows: FlowsList,
            command_processor: CommandProcessor,
            action_runner: ActionRunner,
            flow_executor: FlowExecutor
    ):
        self.flows = flows
        self.command_processor = command_processor
        self.action_runner = action_runner
        self.flow_executor = flow_executor

    async def handle(self, commands: list[Command], state: DialogueState) -> list[BotMessage]:
        # 阶段1：CommandProcessor 进行状态的修改
        self.command_processor.run(commands, state, self.flows)

        # 阶段2：FlowExecutor 进行任务/流程的推进
        messages = await self.flow_executor.run_task(state, self.flows, self.action_runner)

        # 返回流程执行器得到的消息
        return messages
