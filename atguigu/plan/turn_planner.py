from __future__ import annotations

import json
import logging
from typing import Any, Dict
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from atguigu.domain.state import DialogueState
from atguigu.task.flow.flows import FlowsList
from atguigu.knowledge.intents import KnowledgeIntent
from atguigu.plan.models import TurnPlan
from atguigu.prompts.history_builder import HistoryBuilder
from atguigu.prompts.loader import load_prompt
from atguigu.infrastructure.llm import llm

# atguigu/plan/turn_planner.py

logger = logging.getLogger(__name__)


class TurnPlanner:
    """
    意图分析器
    作用：根据任务自然语言 调用LLM 分析轨道类型
    """

    async def predict(self, state: DialogueState, flows: FlowsList, intents: Dict[str, KnowledgeIntent]) -> TurnPlan:
        """

        :param state:
        :return: 返回值是什么?(分析:定义数据模型)
        """

        # 1. 构建提示词
        inputs_prompt = self._build_prompt_inputs(state, flows, intents)

        # 2. 调用LLM模型
        turn_plan = await  self._predict_from_prompt_inputs(inputs_prompt)

        return turn_plan

    def _build_prompt_inputs(self, state: DialogueState, flows_list: FlowsList, intents: Dict[str, KnowledgeIntent]) -> Dict[str, Any]:
        """
        构建提示词输入参数
        :param state:
        :param flows_list:
        :return:
        """
        # 1. 用户消息
        user_msg = HistoryBuilder._render_user_message(state.pending_turn.user_message)

        # 2. 历史对话(当前session的turns:后10轮：最近的10轮) 。历史对话取多少 取哪些：动态策略
        current_conversation = HistoryBuilder.build(state.current_session().turns[-10:])

        # 3. 当前激活任务(业务任务)
        active_task_json = json.dumps(
            state.active_task.model_dump(mode="json"),ensure_ascii=False
        ) if state.active_task is not None else None

        # 4. 中断任务
        interrupted_tasks_json = json.dumps(
            [paused_task.model_dump(mode="json") for paused_task in state.paused_tasks],
            ensure_ascii=False
        )

        # 5. 页面点击卡片获取的信息
        focused_object_json = json.dumps(state.focused_object.model_dump(mode="json")) if state.focused_object is not None else None

        # 6. 流程清单
        # available_flows_json=[{} for flow in flows_list.flows if not flow.id.startswith("system_")]

        available_flows_json = json.dumps(
            {
                "flows": [{k: v for k, v in flow.model_dump(mode="json").items() if k != "steps"} for flow in flows_list.flows if not flow.id.startswith("system_")]
            },
            ensure_ascii=False)

        return {
            "user_message": user_msg,
            "current_conversation": current_conversation,
            "active_task_json": active_task_json,
            "interrupted_tasks_json": interrupted_tasks_json,
            "focused_object_json": focused_object_json,
            "available_flows_json": available_flows_json,
            "knowledge_intents_json": json.dumps([{ "id": i.id, "description": i.description } for i in intents.values()], ensure_ascii=False)
        }

    async def _predict_from_prompt_inputs(self, inputs_prompt: Dict[str, Any]) -> TurnPlan:
        prompt_template_text = load_prompt("turn_plan")
        prompt_template = PromptTemplate.from_template(
            template=prompt_template_text, template_format="jinja2"
        )
        chain = prompt_template | llm | JsonOutputParser()

        try:
            response = await chain.ainvoke(inputs_prompt)
        except OutputParserException:
            logger.warning("意图规划未返回有效 JSON，将请求澄清")
            return TurnPlan()

        if not isinstance(response, dict):
            logger.warning("意图规划的根节点不是对象，将请求澄清")
            return TurnPlan()

        try:
            return TurnPlan.from_dict(response)
        except (KeyError, TypeError, ValueError) as exc:
            logger.warning("意图规划结构无效（%s），将请求澄清", type(exc).__name__)
            return TurnPlan()
