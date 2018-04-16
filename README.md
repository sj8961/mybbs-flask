Cnode-like bbs
----------------------
- 论坛实现包括注册、登录、上传头像、修改签名，以及发表博客、评论、私信等功能
- 基于MVC架构，Flask 实现后端路由与API，基于Mongodb 的ORM 实现存储数据，模板渲染则使用Jinja2
- Redis 存储随机参数 token 验证防御 CSRF攻击，转义输入防御XSS攻击
- 部署使用 Nginx+Guincorn，提供反向代理、压缩静态文件、缓存服务，实现多进程负载均衡，提升性能
- 使用 Vagrant实现环境一致化，Shell 脚本实现一键部署
-
-


-![image](https://github.com/sj8961/mybbs-flask/blob/master/user_image/mybbs-flask.gif)
