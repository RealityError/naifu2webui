## 🍭naifu2webui - 一个naifu前端接入webui端的设想
### 😊简介： 
#### naifu的前端相对于webui有着更为简洁的界面和更为优秀的蒙版，不仅很适合普通的用户使用，也可以实现前后端分离，方便管理。于是，在群友们的支持下，我开启了该项目。
### 🙌注意：
#### 1.本项目通过webuiapi实现，请在config.yaml中填入对应信息，并开启webui的api。
#### 2.本人水平有限，代码可能会出现一些影响使用的bug，欢迎大家提issue共同讨论。
#### 3.关于数据库的使用，下面会给出例子：

```python
#在代码中使用
#导入数据库
from sql_whitecat import sql_neko
#初始化数据库，如果不存在，会按照config.yaml的信息创建
text = sql_neko()
#添加用户，user_id默认为QQ号
text.execute_sql("add_user",("2029354033","cat"))
#通过user_id查用户，改变token
text.execute_sql("change_user_token",("helpme","2029354033"))
#通过token查user_id
print(text.Query_sql("token2user","helpme"))
#请注意！数据库查询结果均为元组，获取单个数据应使用[0]

```

### 💯 TODO
## 2023/2/9
### 1.重写翻译模块 。
### 2.增加对蒙版的支持。
### 3.增加对webui功能的支持(如：xy图，高清修复等)。