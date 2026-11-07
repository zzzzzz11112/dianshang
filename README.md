# 电商小二 · AI 电商客服系统

一个基于 **Vue 3、FastAPI、LangChain 和 MySQL** 的电商客服学习项目。系统通过大模型理解用户意图，再结合 YAML 任务流程和电商业务接口，处理订单查询、物流查询、商品咨询和多轮对话。

仓库包含前端、客服后端、电商中台和数据库初始化配置，可以在本地启动完整的演示环境。

## 功能概览

| 功能 | 当前实现 |
| --- | --- |
| 订单状态查询 | 收集订单号，调用中台接口，返回订单状态与摘要 |
| 物流查询 | 查询物流公司、运单号及物流状态 |
| 商品信息咨询 | 基于选中的商品卡片获取商品数据，再生成自然语言回复 |
| 多轮任务 | 收集槽位信息，支持任务打断、挂起、取消和恢复 |
| 对象消息 | 支持将订单、商品卡片作为当前讨论对象，并用于自动填槽 |
| 历史消息 | 使用 MySQL 保存对话状态和历史消息 |
| 闲聊与澄清 | 处理日常问候，并在意图不明确或规划校验失败时追问 |
| 退款申请演示 | 收集订单号与退款原因，返回演示确认；尚未接入退款操作接口 |

### 当前实现边界

- FAQ 和 RAG 保留提供者接口，目前尚未接入实际知识库。
- 相似商品推荐、人工客服转接目前为占位回复。
- 前端有语音播放按钮，但客服后端尚未实现 `/api/chat/tts`。
- 电商中台提供退款申请记录和催发货记录的创建接口，客服任务流程尚未调用这些写入接口。
- 当前版本面向学习和本地演示，尚未实现完整的用户认证、资源访问授权与生产部署配置。

## 系统架构

```mermaid
flowchart LR
    User[用户] --> Web[Vue 3 前端<br/>5173]
    Web -->|/api| Customer[FastAPI 客服后端<br/>18082]
    Web -->|/commerce| Commerce[电商中台<br/>18081]
    Customer --> Planner[意图规划与校验]
    Planner --> Task[任务流程 Task]
    Planner --> Knowledge[知识咨询 Knowledge]
    Planner --> Chitchat[闲聊 Chitchat]
    Task --> Commerce
    Knowledge --> Commerce
    Planner --> LLM[大模型服务]
    Knowledge --> LLM
    Chitchat --> LLM
    Customer --> History[(customer_service<br/>对话状态与历史)]
    Commerce --> Business[(commerce<br/>用户、订单、商品、物流)]
```

一次文本消息的主要处理过程：

1. 加载用户的对话状态，准备当前会话。
2. 大模型生成本轮规划，选择任务、知识咨询或闲聊轨道。
3. 校验规划中的轨道、流程与知识意图。
4. 推进任务流程，或查询业务数据并生成回复。
5. 保存对话状态，返回本轮消息。

业务任务由 `flow_config/` 中的 YAML 描述。Python 代码负责状态管理、流程执行和动作调用，提示词模板负责组织模型输入。

## 技术栈

| 部分 | 技术 |
| --- | --- |
| 前端 | Vue 3、Vite、JavaScript |
| 客服后端 | FastAPI、Pydantic、LangChain、Jinja2 |
| 流程配置 | YAML、PyYAML |
| 数据访问 | SQLAlchemy、aiomysql、PyMySQL |
| 数据库 | MySQL 8.4 |
| 环境与依赖 | uv、npm、Docker Compose |
| 模型接入 | 通过 LangChain 调用 OpenAI 兼容接口，示例使用 Qwen |

## 项目结构

```text
dianshang/
├── atguigu/                         # 客服后端
│   ├── api/                         # 请求模型、路由和依赖注入
│   ├── conf/                        # 环境变量配置
│   ├── domain/                      # 消息、上下文和对话状态
│   ├── engine/                      # 对话引擎与消息分发
│   ├── plan/                        # 本轮意图规划与校验
│   ├── task/                        # 命令、任务流程及动作执行
│   ├── knowledge/                   # 商品、订单等知识提供者
│   ├── chitchat/                    # 闲聊回复
│   ├── clarify/                     # 澄清回复
│   ├── prompts/                     # 提示词加载与 Jinja2 模板
│   ├── models/                      # 客服数据库模型
│   ├── repository/                  # 对话状态持久化
│   └── infrastructure/              # 模型、HTTP 客户端与数据库连接
├── customer-service-frontend/       # Vue 前端
├── ecommerce-service-backend/       # 电商中台及其独立依赖环境
├── flow_config/                     # 业务流程与系统流程定义
├── docker/
│   ├── docker-compose.yml           # MySQL 容器配置
│   ├── mysql/initdb/                # Docker 首次初始化 SQL
│   └── windows/initdb/              # 本机 MySQL 初始化 SQL
├── .env.example                     # 客服环境变量示例
├── main.py                          # 客服后端启动入口
├── pyproject.toml                   # 客服 Python 依赖
├── uv.lock                          # 客服依赖锁文件
└── README-全栈启动.md               # 补充启动说明
```

## 本地运行

### 1. 环境准备

- Git。
- Python **3.12**：电商中台当前要求 `>=3.12,<3.13`；客服后端支持 `>=3.12`。
- uv。
- Node.js **22 或 24**，以及 npm。
- Docker Desktop 和 Docker Compose，或自行准备可连接的 MySQL。
- 有效的模型 API Key，以及与之匹配的模型名称和接口地址。

以下命令使用 Windows PowerShell。首次安装 Python/npm 依赖及拉取 Docker 镜像需要联网。

### 2. 获取项目

```powershell
git clone https://github.com/zzzzzz11112/dianshang.git
cd dianshang
```

如果已经下载项目，直接进入项目根目录即可。

### 3. 启动 MySQL

先打开 Docker Desktop，等待其启动完成，然后在项目根目录执行：

```powershell
docker compose -f .\docker\docker-compose.yml up -d
docker compose -f .\docker\docker-compose.yml ps
```

配套配置使用本机 **3307** 端口映射到容器的 3306 端口。首次初始化数据卷时，会执行 `docker/mysql/initdb/` 下的 SQL，创建 `customer_service`、`commerce` 两个数据库及示例数据。

已有数据卷时，重启容器不会再次执行初始化 SQL。

### 4. 配置环境变量

如果 `.env` 尚不存在，从示例复制。已有配置时保留原文件：

```powershell
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
}
if (-not (Test-Path .\ecommerce-service-backend\.env)) {
    Copy-Item .\ecommerce-service-backend\.env.example .\ecommerce-service-backend\.env
}
```

**客服后端：项目根目录 `.env`**

```dotenv
LLM_MODEL=qwen-plus
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_API_KEY=your_api_key

COMMERCE_API_BASE_URL=http://127.0.0.1:18081
DATABASE_URL=mysql+aiomysql://atguigu:Atguigu.123@127.0.0.1:3307/customer_service?charset=utf8mb4

APP_HOST=127.0.0.1
APP_PORT=18082
```

将 `your_api_key` 替换为自己的密钥。使用其他模型服务时，同时调整 `LLM_MODEL` 和 `LLM_BASE_URL`。

**电商中台：`ecommerce-service-backend/.env`**

```dotenv
DATABASE_URL=mysql+pymysql://atguigu:Atguigu.123@127.0.0.1:3307/commerce?charset=utf8mb4
APP_HOST=127.0.0.1
APP_PORT=18081
```

以上数据库账号与端口对应仓库自带的 Docker 配置。原始 `.env.example` 使用本机 MySQL 配置，复制后需要按上述内容调整。

两个服务的连接方式不同：**客服使用 `aiomysql` 和 `customer_service` 数据库，中台使用 `pymysql` 和 `commerce` 数据库。**

如果使用自行安装的 MySQL，请按实际连接信息配置，并执行 `docker/windows/initdb/` 下的初始化 SQL。

### 5. 启动电商中台

打开终端一，进入项目根目录，再执行：

```powershell
cd ecommerce-service-backend
uv sync --python 3.12
uv run python main.py
```

等待出现 `Application startup complete`。

- [中台接口文档](http://127.0.0.1:18081/docs)
- [中台健康检查](http://127.0.0.1:18081/health)

### 6. 启动客服后端

打开终端二，进入项目根目录执行：

```powershell
uv sync --python 3.12
uv run python main.py
```

等待出现 `Application startup complete`。接口文档：[客服 API](http://127.0.0.1:18082/docs)。

两个后端各自维护自己的 `.venv`。如果根目录已有符合要求的虚拟环境，也可以直接执行 `uv sync`。

### 7. 启动前端

打开终端三，进入项目根目录，再执行：

```powershell
cd customer-service-frontend
npm.cmd ci
npm.cmd run dev
```

浏览器访问 **[电商客服界面](http://127.0.0.1:5173)**。

三个终端均需保持运行。修改 `.env` 后，应在对应后端终端按 `Ctrl+C`，再重新执行启动命令。

## 使用示例

页面默认使用示例用户 `u1001`。启动服务并确认数据库初始化完成后，可以按以下方式体验：

1. 在右侧选择一张商品卡片并发送，输入“商品信息”或“这个商品多少钱”。
2. 选择订单卡片，输入“查询订单状态”或“帮我查物流”。
3. 输入“我要退款”，按提示提供订单号和原因，体验槽位收集流程。
4. 在任务中途切换业务，再通过“继续刚才的任务”体验挂起与恢复。

示例商品 ID：`SKU10001`；示例订单号：`A20260410001`。

## 接口说明

### 客服服务

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| POST | `/api/chat` | 发送文本或对象消息 |
| GET | `/api/chat/history?sender_id=u1001` | 获取用户历史消息 |

发送商品卡片的请求体：

```json
{
  "sender_id": "u1001",
  "object": {
    "type": "product",
    "id": "SKU10001",
    "title": "iPhone 15 Pro 256G 远峰蓝"
  }
}
```

随后使用同一 `sender_id` 发送文本：

```json
{
  "sender_id": "u1001",
  "text": "商品信息"
}
```

响应结构如下，实际回复取决于当前业务数据、上下文和模型输出：

```json
{
  "sender_id": "u1001",
  "message_id": "服务端生成的消息ID",
  "messages": [
    {
      "text": "根据商品数据生成的回复",
      "object": null
    }
  ]
}
```

### 电商中台

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| GET | `/health` | 检查服务及数据库连接 |
| GET | `/users/{user_id}/orders` | 用户近期订单 |
| GET | `/users/{user_id}/products` | 用户相关商品 |
| GET | `/orders/{order_id}` | 订单详情 |
| GET | `/orders/{order_id}/status` | 订单状态 |
| GET | `/orders/{order_id}/logistics` | 物流信息 |
| GET | `/products/{product_id}` | 商品详情 |
| POST | `/orders/{order_id}/shipping-reminders` | 创建催发货记录 |
| POST | `/orders/{order_id}/refund-applications` | 创建退款申请记录 |

完整参数和响应模型可在各服务的 `/docs` 页面查看。

## 常见问题

| 现象 | 排查方法 |
| --- | --- |
| 访问 `18081` 或 `18082` 首页出现 404 | 这两个端口提供 API；访问 `/docs` 查看接口，前端页面使用 `5173` |
| 前端提示无法连接 `18082` | 检查客服后端是否出现 `Application startup complete`，并保持终端运行 |
| 提示 `The loaded 'pymysql' is not async` | 根目录 `.env` 的客服数据库驱动应为 `mysql+aiomysql` |
| 中台返回 500 或无法读取订单 | 检查中台日志、数据库账号、数据库名称及端口；配套 Docker 使用本机 `3307` |
| 修改 `.env` 后仍报旧错误 | 完整停止并重启对应后端，确保重新加载配置 |
| 模型鉴权、余额或模型名称报错 | 检查密钥是否有效，以及模型名称、接口地址是否属于同一服务 |
| 页面没有示例订单 | 确认初始化 SQL 已执行，当前用户可使用 `u1001` |
| 点击语音按钮没有播放 | 当前客服后端尚未提供 TTS 接口 |

## 开发与扩展

- **调整业务流程**：修改 `flow_config/user_flows.yml`，通过步骤、槽位和动作定义业务。
- **新增业务动作**：在 `atguigu/task/action/custom/` 中实现 `Action` 子类，并在流程 YAML 中引用其名称。
- **扩展知识来源**：在 `atguigu/knowledge/providers.py` 中实现知识提供者，并配置意图与提供者的映射。
- **调整提示词**：编辑 `atguigu/prompts/jinja2/` 中的模板。
- **构建前端**：在 `customer-service-frontend/` 中运行 `npm.cmd run build`，生成 `dist/`。

前端开发服务器通过代理将 `/api` 转发至客服后端，将 `/commerce` 转发至中台。部署前端构建产物时，需要为这些路径配置相应的服务转发。

真实 `.env`、`.venv/`、`node_modules/` 和构建产物已列入 `.gitignore`。仓库保留 `.env.example` 和依赖锁文件，便于重新配置运行环境。

