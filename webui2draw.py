import requests

from log import logger
from model import GenerationRequest
from config import config


class webui_(object):

    data: dict
    api_web: str

    def __init__(self,request: GenerationRequest) -> None:
        #用http协议
        self.api_web = "http://"+config["webui_api"]
        self.data = {
            # webui高清修复选项
            "enable_hr": False,
            "restore_faces": False,
            "tiling": False,
            # text2img主要条件(按webui从上往下排列)
            "prompt": request.prompt,
            "negative_prompt": request.uc,
            "steps": request.steps,
            "sampler_index": "DDIM",
            "width": request.width,
            "height": request.height,
            "cfg_scale": request.scale,
            "seed": request.seed,
             # TODO(me): 这里记得写预设样式匹配
            "styles": [
            ],
            # 生成几张图
            "batch_size": request.n_samples,
            # 高清修复（Highres. fix）的参数
            "firstphase_width": 0,
            "firstphase_height": 0,
            "denoising_strength": 0,
            #未使用的内容
            # # Extra内容
            # "subseed": -1,
            # "subseed_strength": 0,
            # "seed_resize_from_h": -1,
            # "seed_resize_from_w": -1,
            # # 插件设置
            # "override_settings": {},
            # # 没搞明白的参数
            # "n_iter": 1,
            # "eta": 0,
            # "s_churn": 0,
            # "s_tmax": 0,
            # "s_tmin": 0,
            # "s_noise": 1,
        }
        #img2img部分
        if request.image != None:
            img_payload = {
                    "init_images": [
                        'data:image/png;base64,' + request.image
                    ],
                    "denoising_strength": request.strength   
                } 
            self.data.update(img_payload)
            self.api_web = self.api_web+"/sdapi/v1/img2img"
            return
        self.api_web = self.api_web+"/sdapi/v1/txt2img"
    def generate(self) -> str:
        #初始变量
        req = requests.post(url = self.api_web,json=self.data)
        if str(req) == "<Response [200]>":
            img_data = req.json()
        return img_data['images']