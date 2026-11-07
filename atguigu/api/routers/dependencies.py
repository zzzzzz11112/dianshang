from __future__ import annotations

from pathlib import Path
from atguigu.plan.turn_planner import TurnPlanner
from atguigu.plan.turn_validator import TurnPlanValidator
from atguigu.task.handler import TaskHandler
from atguigu.task.command.processor import CommandProcessor
from atguigu.task.flow.loader import FlowLoader
from atguigu.task.flow.executor import FlowExecutor
from atguigu.task.action.builder import build_action_runner
from atguigu.knowledge.handler import KnowledgeHandler
from atguigu.knowledge.intents import KNOWLEDGE_INTENTS
from atguigu.knowledge.registry import KnowledgeProviderRegistry
from atguigu.knowledge.providers import ProductAPIProvider, OrderAPIProvider, FAQProvider, RAGProvider
from atguigu.knowledge.responder import KnowledgeResponder
from atguigu.chitchat.handler import ChitChatHandler
from atguigu.chitchat.responder import ChitChatResponder
from atguigu.clarify.responder import ClarifyResponder

# atguigu/api/dependencies.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from atguigu.service.dialogue_service import DialogueService
from atguigu.repository.dialogue_state_repository import DialogueStateRepository
from atguigu.engine.dialogue_engine import DialogueEngine
from atguigu.infrastructure import database



async def get_session():
    """
    实际流程：
        进入 async with → 打开 session
        yield session → 把 session 交给repository函数使用
        路由函数执行完毕 → 回到 yield 之后
        退出 async with → 自动关闭 session ✅
    :return:
    """
    async with database.async_session() as session:  # 异步方式获取session  获取session要网络传输（耗时的）
        yield session


async def get_dialogue_state_repository(session: AsyncSession = Depends(get_session)):
    """
    创建 DialogueStateRepository 实例

    依赖链执行顺序：
       1. get_session() 打开 session 并 yield
       2. 这里拿到 session，创建 Repository
       3. Repository 被Service使用，Service被路由函数使用
       4. 路由函数返回后，get_session() 继续执行，自动关闭 session
    :param session:
    :return:
    """
    return DialogueStateRepository(session=session)
    # 3. 函数返回后，FastAPI 继续执行 get_session() y


async def get_engine():
    base_path = Path(__file__).resolve().parents[3]
    flow_list = FlowLoader().load_many([
        base_path / "flow_config" / "user_flows.yml",
        base_path / "flow_config" / "system_flows.yml",
    ])
    # atguigu/api/routers/dependencies.py
    return DialogueEngine(
        turn_planner = TurnPlanner(),
        task_handler = TaskHandler(
            flows=flow_list,
            command_processor=CommandProcessor(),
            action_runner=build_action_runner(),
            flow_executor=FlowExecutor()
        ),
        knowledge_handler = KnowledgeHandler(
            knowledge_intents=KNOWLEDGE_INTENTS,
            knowledge_responder=KnowledgeResponder(),
            provider_registry=KnowledgeProviderRegistry(
                [
                    ProductAPIProvider(),
                    OrderAPIProvider(),
                    FAQProvider(),
                    RAGProvider(),
                ]
            ),
        ),
        clarify_responder = ClarifyResponder(),
        turn_plan_validator = TurnPlanValidator(),
        chitchat_handler=ChitChatHandler(ChitChatResponder())
    )

async def get_dialogue_service(
        dialogue_state_repository: DialogueStateRepository = Depends(get_dialogue_state_repository),
        dialogue_engine: DialogueEngine = Depends(get_engine)
) -> DialogueService:
    return DialogueService(dialogue_state_repository=dialogue_state_repository, dialogue_engine=dialogue_engine)
