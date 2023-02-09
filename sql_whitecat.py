# -*- coding: utf-8 -*-
# @Time : 2023/2/7
# @Author : 白猫猫
# @File : sql_whitecat.py
# @Software: Vscode|虚拟环境|3.10.6|64-bit
"""该模块定义了通用SQLite数据库的增删改查功能


"""

import os
import sqlite3
from log import logger
from config import config

class sql_neko(object):

    sql_name: str  = config["sql"]["name"]
    connect = None
    cursor = None
    def __init__(self) -> None:
        """
        数据库初始化函数

        """
        if os.path.exists("./sql/"+self.sql_name+".db") is False:
            logger.info("未创建数据库，创建中----")
            try:
                connect = sqlite3.connect("./sql/"+self.sql_name+".db")                                
                cursor = connect.cursor()
            except Exception as e:
                logger.info("初始化时，连接数据库表失败,错误如下:"+str(e))
            #创建用户表
            sql_init1 = """CREATE TABLE user(
                id integer primary key autoincrement,
                user_id  varchar not null unique,
                token varchar(20) not null,
                pic_num integer
            )"""
            #创建图片对照表 
            sql_init2 = """CREATE TABLE pic(
                id integer primary key autoincrement,
                user_id  varchar not null,
                token varchar(20) not null,
                pic_name integer,
                pic_info varchar not null
            )"""
            try:
                cursor.execute(sql_init1)
                cursor.execute(sql_init2)
                cursor.close()
                connect.commit()
                connect.close()
            except Exception as e:
                logger.info("初始化时，创建数据库表失败,错误如下:"+str(e))
            
        try:
            self.connect = sqlite3.connect("./sql/"+self.sql_name+".db")  
            self.cursor = self.connect.cursor()
            logger.info("数据库启动成功")
        except Exception as e:
            logger.info("数据库初始化失败,错误如下:"+str(e))
    def execute_sql(self,action:str,data:list)-> bool:
        """
        数据库的插入、修改函数
        - param action: 行为 

        格式：["add_user","add_pic","change_user_data"]
        
        add_user:(user_id,token)

        add_pic:(user_id,token,pic_name,pic_info)

        change_user_token:(user_id,newtoken)

        change_user_picnum:(new_pic_num,token)

        - data: 传入数据
        return: 返回操作数据库状态
        
        """
        if self.connect == None or self.cursor == None:
            logger.info("未初始化!")
            return False
        if action == "add_user":
            sql_ac = "insert into user(user_id,token,pic_num) values(?,?,0);"
            sql_data = [data]
            try:
                self.cursor.executemany(sql_ac, sql_data)
                self.connect.commit()
                logger.info("添加用户成功")
                return True
            except Exception as e:
                logger.info("添加用户失败,错误如下:"+str(e))
                return False
        elif action == "add_pic":
            sql_ac = "insert into pic(user_id,token,pic_name,pic_info) values(?,?,?,?);"
            sql_data = [data]
            try:
                self.cursor.executemany(sql_ac, sql_data)
                self.connect.commit()
                logger.info("添加图片成功")
                return True
            except Exception as e:
                logger.info("添加图片失败,错误如下:"+str(e))
                return False
        elif action == "change_user_token":
            sql_ac = "UPDATE user SET token = '"+data[0]+"' WHERE user_id = '"+data[1]+"'"
            try:
                self.cursor.execute(sql_ac)
                self.connect.commit()
                logger.info("新token设置成功")
                return True
            except Exception as e:
                logger.info("用户设置失败,错误如下:"+str(e))
                return False
        elif action == "change_user_picnum":
            sql_ac = "UPDATE user SET pic_num = '"+data[0]+"' WHERE token = '"+data[1]+"'"
            try:
                self.cursor.execute(sql_ac)
                self.connect.commit()
                logger.info("新用户生成图数设置成功")
                return True
            except Exception as e:
                logger.info("用户设置失败,错误如下:"+str(e))
                return False    

        
        logger.info("有未被识别的命令，请检查代码")
        return False
    def del_sql(self,action:str,data:list)-> bool:  
        """
        TODO: 还没想好删除功能拿来干什么,有需求了再写
        
        """
        if self.connect == None or self.cursor == None:
            logger.info("未初始化!")
            return False
        pass
    def Query_sql(self,action:str,data:str)-> tuple:
        """
        数据库的查询函数
        - param action: 行为 
        格式：["user_picnum","user_pic","token2user","token2picnum"]
        - data: int 用户id

        return: 返回元组
        
        """
        if self.connect == None or self.cursor == None:
            logger.info("未初始化!")
            return False
        if action == "user_picnum":
            sql_ac = "select pic_num from user where user_id='"+str(data)+"'"
            self.cursor.execute(sql_ac)
            return self.cursor.fetchone()
        if action == "token2picnum":
            sql_ac = "select pic_num from user where token='"+str(data)+"'"
            self.cursor.execute(sql_ac)
            return self.cursor.fetchone()
        
        if action == "token2user":
            sql_ac = "select user_id from user where token='"+data+"'"
            #logger.debug(sql_ac)
            self.cursor.execute(sql_ac)
            return self.cursor.fetchone()


        if action == "user_pic":
            sql_ac = "select * from pic where user_id='"+str(data)+"'"
            self.cursor.execute(sql_ac)
            return self.cursor.fetchall()
    def close_sql(self)-> None: 
        if self.connect == None or self.cursor == None:
            logger.info("未初始化!")
            return False
        self.connect.close()

