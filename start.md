# Flask 项目简介

## project structure 项目文件夹结构

Project

-- 文件夹

|---app 所有的功能都在这个文件夹下

      -- 文件夹

      |--- common    公共功能模块的代码都在这里， 每个公共模块 一个 py 文件
      |--- libs    第三方的库
      |--- modules  功能模块，每个功能模块 一个 py 文件
      |--- templates  html 页面
      |--- model  数据库的模型，用来存储数据

      -- 文件
      |--- __init__.py   启动 flask app 是需要的文件
      |--- config.py  app 系统的参数设置
      |--- 其他文件。。。 还可以有其他的 py 文件

|---log 这个文件夹里放 log 文件

|---files 放一些文件，比如用户上传的文件

|---migrations 数据库升级时自动创建的文件夹，一般不用

-- 文件

|--- manage.py 启动 Flask 项目用的文件

|--- req.txt python 环境需要的 libs 清单

|--- start.sh 在服务器上，执行这个文件就启动 flask 了

## 本地开发和调试的命令

###常用命令

**命令**
`python manage.py`

    如果不带参数，则显示 这个命令可以有的参数：

      db  数据库相关命令
      shell  用命令行方式启动 flask， debug 时用
      runserver 启动本地服务器

**用命令行方式启动 flask**

`python manage.py shell`

用命令行方式启动 flask， debug 时用
比如：直接执行 flask 模块里的 fuuntion

```
>> from myapp.modules.api import *
>> helps()

```

**启动 flask 服务器**

`python manage.py runserver`

执行后，会在本地启动 flask 服务， 你可以用浏览器访问 flask 项目了

地址： http://127.0.0.1:5000/ (Press CTRL+C to quit)

      `python manage.py shell`

**数据库相关命令**

**初始化数据库**

`python manage.py db init`

flask 会 根据 **model/models.py** 里的模型，建立数据库。第一次建立数据库时使用这个命令，以后就不用了。

如果要重新建立数据库， 可以先把 **migrations** 这个文件夹删除，再允许此命令，就重新建数据库了.

这里的 “重建数据库”， 其实并没有把数据库服务器上的文件删除，只是根据 **models.py** 的 **class** 更新数据库结构，并不会删除数据库里的数据

**model.py 修改后，更新数据库**

```
python manage.py db migrate -m some_comments

python manage.py db upgrade

```

some_comments 是本次升级的简单备注，成功后，会在**migrations**下生成 升级的 py 文件

# 在服务器上部署 flask

步骤：

1. 上传文件到服务器

2. 设置项目

   2.1 设置 python 的环境， 依赖库

   2.2 设置 production 环境的数据库连接，每次修改过 **models.py** 后要 **migrate ， upgrade**

3. 在 /etc/nginx 下设置服务器的域名和文件夹

4. 启动服务器

## 在服务器上启动 flask

`gunicorn -w 4 -b 127.0.0.1:9090 manage:app`

或者，把这个命令写进 **start.sh** 文件， 直接执行

`.start.sh`

9090 是服务器上的端口，
