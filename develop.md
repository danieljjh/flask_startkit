# Flask develop Tutorial

## Flask 后台的用途

### 作为后台服务器

1. 你创建 一些 http API， 然后可以通过（小程序， web ajax） 发送 http request 请求给服务器，让服务器执行指令， 并把后台指令的执行结果，通过 API 返回

2. 利用 flask 执行一些后台任务， 把结果保存在数据库， 或者，把执行结果通过 email， 短信，或其他 消息工具 传送给你

## Step by Step

### 1. 创建一个 api，向服务器发送 request ，并获得 response

**1.1 http get 请求**

- 在 **modules** 下新建一个文件 **api.py**

- 创建 一个 接口 网址，处理 get 请求

- 在浏览器里输入请求
  `http://localhost:5000/api/my_get?name=yale&age=14`

**1.2 http post 请求**

- 创建一个 api ，向服务器发送 POST request, 得到 response

- POST 请求示例 `http://localhost:5000/api/my_post`

### 2. 创建一个网页，在网页上显示后台产生的数据

参见 `modules/page.py`

- /pages/home 基本页面 + 后台向页面传递参数 + 跳转连接

- /pages/hello_yale 带参数的页面， 用 jquery Ajax 发送请求 示例

- /pages/a_form 表单提交示例

## Some docs

[Flask tutorials](https://realpython.com/tutorials/flask/)

[exploreflask](http://exploreflask.com/en/latest/views.html)
