# 电商小二：前端、客服后端与电商中台

项目目录：`D:\develop\PyCharm 2026.1\project\PythonProject\dianshang`。

| 组件 | 所在目录 | 默认地址 |
| --- | --- | --- |
| 客服后端 | 项目根目录，代码在 `atguigu/` | http://127.0.0.1:18082 |
| Vue前端 | `customer-service-frontend/` | http://127.0.0.1:5173 |
| 电商中台 | `ecommerce-service-backend/` | http://127.0.0.1:18081 |
| MySQL初始化与Docker配置 | `docker/` | Docker映射到本机3307端口 |

以下命令均在项目根目录开始执行。前端和两个后端分别在独立终端中启动。
客服后端支持Python 3.12及以上，中台的原始依赖要求Python 3.12；建议两个后端均使用3.12。
各后端使用各自目录中的`.venv`，无需移动根目录已有的虚拟环境。

## 1. 准备数据库与环境变量

根目录`.env`供客服后端使用，`ecommerce-service-backend/.env`供中台使用。
中台`.env`已从原始示例复制；根目录`.env`保持原样。
客服后端还需要填写有效的`LLM_API_KEY`等模型配置。

如果使用本机MySQL，按实际账号、密码及端口修改两个`.env`的`DATABASE_URL`。
课程示例默认是本机3306端口、root账号、密码123456；两个数据库分别为`customer_service`和`commerce`。
在MySQL客户端依次执行`docker/windows/initdb/001_init_customer_service.sql`和`002_init_commerce.sql`以创建表和示例数据。

如果使用配套Docker MySQL，可在确认本机3307端口可用后执行：

```powershell
docker compose -f .\docker\docker-compose.yml up -d
```

首次创建该Docker数据卷时会自动执行`docker/mysql/initdb/`中的SQL。
Docker配置与课程原始`.env.example`的账号和端口不同。使用Docker时，将两个`.env`中的数据库地址分别改为：

```dotenv
# 根目录 .env
DATABASE_URL=mysql+aiomysql://atguigu:Atguigu.123@127.0.0.1:3307/customer_service?charset=utf8mb4
# ecommerce-service-backend/.env
DATABASE_URL=mysql+pymysql://atguigu:Atguigu.123@127.0.0.1:3307/commerce?charset=utf8mb4
```

## 2. 启动电商中台（终端一）

```powershell
Set-Location .\ecommerce-service-backend
uv sync --python 3.12
uv run python main.py
```

在中台目录中运行，使其读取自己的`.env`。接口文档为 http://127.0.0.1:18081/docs 。
原材料README中的`app.main:app`与源码目录不符，已改为实际存在的`main.py`入口。

## 3. 启动客服后端（终端二）

```powershell
uv sync --python 3.12
uv run python main.py
```

在项目根目录中运行。确认根目录`.env`中的`COMMERCE_API_BASE_URL=http://127.0.0.1:18081`。
接口文档为 http://127.0.0.1:18082/docs 。

## 4. 启动前端（终端三）

```powershell
Set-Location .\customer-service-frontend
npm ci
npm run dev
```

浏览器访问 http://127.0.0.1:5173 。`vite.config.js`已将`/api`代理到18082，`/commerce`代理到18081。
如需生成前端构建产物，在前端目录运行`npm run build`。

## 本次导入范围

前端和中台源码、锁文件、图片资源、Docker配置与数据库初始化SQL均来自原配套资料。
未复制第三方依赖目录、虚拟环境或Python缓存；未安装依赖或启动服务。
前端提供的语音播放按钮依赖`/api/chat/tts`接口，课堂笔记整理的客服后端尚未实现此接口。
客服后端的FAQ、RAG和退款演示实现范围见根目录`README.md`。
