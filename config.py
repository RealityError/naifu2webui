# -*- coding: utf-8 -*-
# @Time : 2023/1/18
# @Author : 白猫猫
# @File : config.py
# @Software: Vscode|虚拟环境|3.10.6|64-bit
"""该模块定义了存储运行设置的变量。
"""
import yaml 

    
config:dict = []   
"""变量存储对象。

默认信息:

- 格式: dict

用法:
python
    ```
    from config import config
    ```
"""
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)