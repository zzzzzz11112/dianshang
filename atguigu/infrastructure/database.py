from __future__ import annotations

# atguigu/infrastructure/database.py

import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine, AsyncEngine

from atguigu.conf.config import settings

# 声明
engine: AsyncEngine | None = None
async_session: async_sessionmaker[AsyncSession] | None = None

# 初始化
def init_db_engine() -> None:
    global engine, async_session

    # 1. 创建异步引擎
    # pool_pre_ping=True
    # 核心作用：自动重连。它能防止程序因为拿到了“过期”或“断开”的连接而报错。
    # 代价：每次使用连接前会多一次极微小的网络交互（发个 ping），但在现代网络环境下，这个开销几乎可以忽略不计。
    # 建议：在生产环境中，强烈建议开启这个选项，它能大大提高程序的稳定性，让你少处理很多莫名其妙的数据库断连错误。
    engine = create_async_engine(settings.database_url, echo=True, pool_pre_ping=True)

    # 2. 创建异步session工厂
    async_session = async_sessionmaker(engine, expire_on_commit=False)

# 关闭资源
async def close_db_engine():
    if engine is not None:
        await engine.dispose()
