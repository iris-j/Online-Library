# Online-Library
An online library for DB project，Django + MySQL + Bootstrap

## 简介
Django的使用模式可以概括为MTV，将应用程序分解为三个组成部分：model，view，template.
使用Django自带的ORM创建数据库结构和实现对数据库的增删查改，避免了直接书写sql语句
### model
处理与数据相关的事务，定义关系数据库的各个字段
### template
前端页面模板，决定前端的显示
### view
连接前后端的桥梁，实现前端用户请求和后端数据库之间的交互

## 技术架构
- 客户端技术：Bootstrap
- 服务端技术：Django Python Web框架
- 数据库：MySQL

## 功能
### 普通读者
#### 无需登录
进入主页，根据图书分类，查看相应的书籍
[!image](https://github.com/iris-j/Online-Library/blob/master/homepage0.png?raw=True)
