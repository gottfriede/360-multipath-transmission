# 服务端

​	一些较为重要的代码文件罗列如下：

### 1. `manage.py`

​	服务端IP地址为 `192.168.246.1` 和 `192.168.242.200` ，启动后端 `Django` 时需修改默认端口号与地址，可使用：

```
python manage.py runserver 0.0.0.0:8080
```

或在 `manage.py` 中添加对应设置：

```
from django.core.management.commands.runserver import Command as Runserver

if __name__ == '__main__':
    Runserver.default_addr = '0.0.0.0'  # modify the default address
    Runserver.default_port = '8080'     # modify the default port

    main()
```



### 2. `core/urls.py` , `backend/urls.py`

​	一些接口路由配置



### 3. `core/api/svc.py`

​	主要实现两个接口 `tile_list` , `download` .

​	请求 `request` 均为 `json` 形式， `tile_list` 应答为 `JsonResponse` , `download` 为 `FileResponse` .