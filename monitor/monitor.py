import uvicorn
import configparser
from fastapi import FastAPI
from getSysInfoG import get_system_usage
import asyncio

# 创建FastAPI应用实例
app = FastAPI()
# 创建一个异步锁
lock = asyncio.Lock()


# 根路径的GET请求
@app.get("/monitor")
async def get_sys_info():
    async with lock:
        data = await get_system_usage()
        return data


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("monitor_config.ini")
    app_port = int(config.get("monitor", "port", fallback=8090))
    uvicorn.run(app, host="0.0.0.0", port=app_port)