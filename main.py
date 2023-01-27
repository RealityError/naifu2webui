# -*- coding: utf-8 -*-
# @Time : 2022/12/14 
# @Author : 白猫猫
# @File : main.py(webui_naifu)
# @Software: Vscode|虚拟环境|3.10.6

'''
基于naifu端的webui，使用webui作为后端生成图片
'''
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import uvicorn
import threading
from webui2draw import webui_
from basetype import *
from config import webui_api
from Trans import trans
from log import logger

genlock = threading.Lock()

import os



#Initialize fastapi
app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logger.info("web服务启动")
    

@app.on_event("shutdown")
def shutdown_event():
    logger.info("web服务关闭")




@app.post('/generate-stream')
async def generate(request: GenerationRequest):
    
    logger.info(request.prompt)
    MP = webui_(webui_api, request)
    data = MP.generate()
    return Response(content=data , media_type="text/event-stream")


@app.get('/')
async def index():
    return FileResponse('static/index.html')

app.mount("/", StaticFiles(directory="static/"), name="static") 

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1", port=11451, log_level="info",workers=4)
