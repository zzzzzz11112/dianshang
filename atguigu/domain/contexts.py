from __future__ import annotations

# atguigu/domain/contexts.py
from typing import Literal, Annotated

from pydantic import BaseModel, Field, TypeAdapter


class TaskContext(BaseModel):
    """
    业务任务上下文
    """
    flow_id: str  # 业务任务的流程ID
    step_id: str | None = None  # 业务任务下的步骤ID
    slots: dict = {}  # 业务任务执行过程中收集到的槽位数据


class SystemContext(BaseModel):
    """
    系统流程上下文
    定义具体流程的通用属性
    """
    flow_id: str  # 系统流程的流程ID
    step_id: str | None = None  # 系统流程当前执行的步骤ID

class StartedSystemContext(SystemContext):
    """
    流程开始
    """
    started_flow_id: str = ""  # 新开始的业务任务ID
    started_flow_name: str = ""  # 新开始的业务任务名字

    # 使用 Literal 类型固定 flow_id 值，作为 Discriminated Union 的区分字段
    flow_id: Literal["system_task_started"] = "system_task_started"

class InterruptedSystemContext(SystemContext):
    """
    流程中断
    """
    interrupted_flow_id: str = ""  # 被中断的旧业务任务ID
    interrupted_flow_name: str = ""  # 被中断的旧业务任务名字
    started_flow_id: str = ""  # 新开始的业务任务ID
    started_flow_name: str = ""  # 新开始的业务任务名字
    flow_id: Literal["system_task_interrupted"] = "system_task_interrupted"

class CanceledSystemContext(SystemContext):
    """
    流程取消
    """
    canceled_flow_id: str = "" # 被取消的业务任务ID
    canceled_flow_name: str = "" # 被取消的业务任务名字
    flow_id: Literal["system_task_canceled"] = "system_task_canceled"

class ResumedSystemContext(SystemContext):
    """
    流程恢复
    """
    resumed_flow_id: str = ""  # 被恢复的业务任务ID
    resumed_flow_name: str = ""  # 被恢复的业务任务名字
    flow_id: Literal["system_task_resumed"] = "system_task_resumed"

class CollectedSystemContext(SystemContext):
    """
    系统流程收集槽位信息
    """
    slot_name: str = ""  # 收集的槽位名
    response: dict = {}  # {"text":"请告诉我你的订单号"}
    flow_id: Literal["system_collect_information"] = "system_collect_information"

# 定义系统流程的联合类型
SystemContextUnion = Annotated[
    StartedSystemContext |
    InterruptedSystemContext |
    CanceledSystemContext |
    ResumedSystemContext |
    CollectedSystemContext,
    Field(discriminator="flow_id")
]
# 创建联合类型适配器实例
system_context_adapter = TypeAdapter(SystemContextUnion)
