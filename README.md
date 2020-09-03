# myblog
fastapi + vue -> myblog  
个人博客 学习试错  

前后端部署都是用Docker进行部署  
待学习K8s  
后端: FastAPI + GINO/Pony ORM/tortoise ORM (ORM的选择有待考虑，目前认为这三种比较合适 GINO和tortoise ORM是支持异步的，Pony ORM同步但是速度很快)  
前端: Vue + Element UI + Nginx部署  

FastAPI文档: https://fastapi.tiangolo.com/  
GINO文档: https://python-gino.org/docs/zh/1.0/index.html  
tortoise ORM文档: https://tortoise-orm.readthedocs.io/en/latest/  
Pony ORM文档: https://docs.ponyorm.org/firststeps.html  
基本上有基础问题都可以在文档中找到解决方案
  
期望功能:  
(×) 1.用户登录  
(×) 2.用户信息可自更新及维护  
(×) 3.用户可发文章  
(×) 4.用户可发评论  
(×) 5.用户可上传文件(包括图片类型，包括视频类型，包括zip等压缩文件类型)  
