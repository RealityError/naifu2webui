# -*- coding:utf-8 -*-
# @Time : 2022/2/3
# @Author : 白猫猫
# @File : main.py(webui_naifu)
# @Software: Vscode|虚拟环境|3.10.6
'''
AI绘画前后端分离的尝试,本项目中使用naifu前端和webuiapi后端
'''

#解决fastapi输出乱码问题（天晓得loguru出了啥bug
from colorama import init
init(autoreset=True)

import os


#导入数据库
from sql_whitecat import sql_neko 

#导入生成
from webui2draw import webui_

import base64
import hashlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
import uvicorn
from starlette.responses import FileResponse
#导入日志模块
from log import logger,LOGGING_CONFIG


#导入类
from model import GenerationRequest

#导入配置
from config import config


app = FastAPI(docs_url=None, redoc_url=None)
"""
fastapi入口,默认关闭docs和redoc文档
"""

#定义中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    #allowed_hosts=["example.com", "*.example.com"]
)



#应用开始终止预设
@app.on_event("startup")
def startup_event():
    
    



    #数据库的处理
    if config["sql"]["open"] == "ON":
        #缓存图片
        global token_png
        images_encoded = []
        token_png  = ""
        ptr = 0
        pic = open("./static/pic/token.png", "rb").read()
        pic = base64.b64encode(pic).decode("ascii")
        images_encoded.append(pic)
        for x in images_encoded:
            ptr += 1
        token_png+= ("event: newImage\nid: {}\ndata:{}\n\n").format(ptr, x)
        #开启数据库接口
        global sql 
        sql = sql_neko()
        @app.get('/sql')
        def sql_data():
            pass
        logger.info("数据库模块已启用")


    logger.info("naifu2webui已启动")
    


@app.on_event("shutdown")
def shutdown_event():
    #数据库的处理
    if config["sql"]["open"] == "ON":
        sql.close_sql()
        logger.info("数据库链接已关闭")
    logger.info("naifu2webui已关闭")


#路径
@app.post('/generate-stream')
async def generate(request: GenerationRequest):

    #文本预处理
    request.prompt = request.prompt.replace("，",",").replace("（","(").replace("）",")").replace("：",":")


    

    
    #token检测
    lst = []
    user_token = ""
    
    if config["sql"]["open"] == "ON":
        for pos,char in enumerate(request.prompt):
            if(char == "*"):
                lst.append(pos)
        
        #没有token
        if lst == []:
            return Response(content=token_png, media_type="text/event-stream") 
        sp_data = request.prompt[lst[0]+1:lst[1]].split(",")
        
        for tmp_str in sp_data:
            if "token" in tmp_str:
                user_token = tmp_str.split(":")[1]
                #logger.debug("测试数值："+user_token)
                tmp = sql.Query_sql("token2user",user_token)[0]
                if tmp == None:
                    return Response(content=token_png, media_type="text/event-stream")
                #移除特殊数值
                request.prompt = request.prompt.replace(request.prompt[lst[0]:lst[1]+1],"")
                
        user_picnum = sql.Query_sql("token2picnum",user_token)[0]
        user_picnum_new = user_picnum + request.n_samples
        sql.execute_sql("change_user_picnum",[str(user_picnum_new),user_token])

            
    #这里在日志中存储信息  
    logger.info(request)
    #绘图类初始化话
    MP = webui_(request)
    #画图获得返回数据
    data_img = MP.generate()
    #处理webui端数据
    data = ""
    ptr = 0
    for i in data_img:
        image = i
        if config["SAVE"]:
            image_s = base64.b64decode(image)   
            hash = str(hashlib.md5(image_s).hexdigest())
            if config["sql"]["open"] == "ON":
                user_id = sql.Query_sql("token2user",user_token)[0]
                if os.path.exists("user_data/"+user_id) is False:
                    logger.info("未创建用户文件夹，创建中----")
                    os.makedirs("user_data/"+user_id)
                with open(r"user_data/"+user_id+"/"+hash +".png", "wb") as fh:
                    fh.write(image_s)
                #logger.info([user_id,user_token,hash +".png",request])
                sql.execute_sql("add_pic",[user_id,user_token,hash +".png",str(request)])
            else:
                with open(r"output/"+hash +".png", "wb") as fh:
                    fh.write(image_s)
    for x in data_img:
        ptr = ptr+1
        data+= ("event: newImage\nid: {}\ndata:{}\n\n").format(ptr, x)    



    return Response(content=data , media_type="text/event-stream")


@app.get('/')
async def index():
    return FileResponse('static/index.html')

app.mount("/", StaticFiles(directory="static/"), name="static") 

if __name__ == "__main__":

    if config["log_save"] == False:
        uvicorn.run("app:app",
                host=config["web"]["host"], 
                port=config["web"]["port"],
                log_level="info",
                )
    else:
        uvicorn.run("app:app",
                host=config["web"]["host"], 
                port=config["web"]["port"],
                log_level="info",
                log_config=LOGGING_CONFIG,
                )