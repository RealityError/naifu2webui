# -*- coding: utf-8 -*-
# @Time : 2023/1/13
# @Author : 白猫猫
# @File : log.py
# @Software: Vscode|虚拟环境|3.10.6|64-bit
"""该模块定义了通用的的日志记录Logger。



"""


from config import config
import loguru
import time

logger = loguru.logger
"""日志记录器对象。

默认信息:

- 格式: `%(asctime)s %(levelname)s %(name)s: %(message)s`
- 等级: `INFO` ，根据 `config.log_level` 配置改变
- 输出: 输出至log文件夹下

用法:
python
    ```
    from log import logger
    ```
"""

default_format: str = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    "{message}"
)
"""默认日志格式"""


logger.add(
    r'./log/data_{time:YYYY_MM_DD}.log', 
    rotation='12 hour',
    level=config["log_level"],
    enqueue=True,
    format=default_format,
    )

time_fmt = "./log/data_"+time.strftime('%Y_%m_%d',time.localtime(time.time()))+".log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": time_fmt
        },
        "access": {
            "formatter": "access",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": time_fmt
 
        },
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}
