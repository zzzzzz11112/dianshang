# 电商小二

此项目由 `D:\ithma\4.视频\day10\课堂笔记` 的01—11章代码片段整理而来，不是从Git仓库克隆的原版源码。
流程配置、依赖和环境变量示例来自 `D:\ithma\2.资料\前端、中台项目\customer-service-backend`。
`SOURCE_MAP.json` 记录代码片段所在笔记与行号。

## 启动

在项目根目录运行（Python 3.12或更高版本）：

```powershell
uv sync
uv run python main.py
```

也可以在PyCharm中选择现有虚拟环境，按 `pyproject.toml` 安装依赖，运行根目录的 `main.py`。
`.env` 已从示例复制，需要自行填写 `LLM_API_KEY`，确认数据库连接。
接口文档：<http://127.0.0.1:18082/docs>。
真实对话依赖LLM服务、MySQL的customer_service数据库和电商中台接口（默认18081端口）。
配套前端、中台和数据库初始化文件已放入本项目，完整启动步骤见 [README-全栈启动.md](README-全栈启动.md)。

## 整理说明

- 合并各章节增量代码，采用第7章的任务恢复逻辑、第9章的执行器和第11章的历史接口。
- 补齐遗漏导入与包目录；统一dependencies路径、commit_turn调用和ResponseDefinition.mode字段。
- 修正笔记中缺失的_validate_task方法名、取消流程ID末尾逗号、无活跃任务时写空槽位等衔接问题。
- SQLAlchemy依赖声明增加asyncio可选依赖，确保安装异步引擎需要的greenlet。
- 系统流程使用带flow_id标签的联合类型保存与恢复，保留过场白所需字段。
- turn_plan.jinja2和chitchat_respond.jinja2未出现在现有笔记及配套资料中，已按接口协议补充，文件内明确标注。
- FAQ、RAG和相似商品推荐保留课程中的占位实现。退款流程也是课程演示回复，未接入真实退款接口。

保留原有.idea和.venv；未安装依赖、未填写真实密钥、未启动外部服务。
