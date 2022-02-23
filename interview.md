# baidu
## 响应状态码
- 301和302状态码区别
  - 301 redirect: 301 代表永久性转移(Permanently Moved)
  - 302 redirect: 302 代表暂时性转移(Temporarily Moved )
- 状态码详细
  - 2XX系列响应代码表明操作成功了
    - 200 OK
    - 201 Created 
    - 202 Accepted 客户端的请求无法或将不被实时处理。请求稍后会被处理。请求看上去是合法的，但在实际处理它时有出现问题的可能
    - 204 No Content 若服务器拒绝对PUT、POST或者DELETE请求返回任何状态信息或表示，那么通常采用此响应代码
  - 3XX系列重定向
    - 300 Multiple Choices 若被请求的资源在服务器端存在多个表示，而服务器不知道客户端想要的是哪一个表示时，发送这个响应代码
    - 301 Moved Permanently 代表永久性转移
    - 302 Temporarily Moved 代表暂时性转移
  - 4XX系列客户端错误
    - 400 Bad Request 这是一个通用的客户端错误状态，当其他4XX响应代码不适用时，就采用400
    - 401 Unauthorized 认证出错
    - 402 Payment Required
    - 403 Forbidden 客户端请求的结构正确，但是服务器不想处理它
    - 404 Not Found 404表明服务器无法把客户端请求的URI转换为一个资源
    - 405 Method Not Allowd 客户端试图使用一个本资源不支持的HTTP方法
    - 406 Not Acceptable 当客户端对表示有太多要求，以至于服务器无法提供满足要求的表示，服务器可以发送这个响应代码。例如：客户端通过Accept头指定媒体类型为application/json+hic，但是服务器只支持application/json
  - 5xx系列服务端错误
    - 500 Internal Server Error
    - 501 Not Implemented 客户端试图使用一个服务器不支持的HTTP特性。
    - 502 Bad Gateway  只有HTTP代理会发送这个响应代码。它表明代理方面出现问题，或者代理与上行服务器之间出现问题，而不是上行服务器本身有问题
    - 503 Service Unavailable 此响应代码表明HTTP服务器正常，只是下层web服务服务不能正常工作
## linux通过端口查进程
  - 根据进程pid查端口
    `lsof -i |grep pid` `netstat -nap |grep pid`
  - 根据端口查进程 
    `lsof -i:port` `netstat -nap |grep port`
## mysql sql执行过程
  - 查询 权限校验 —> 查询缓存 —> 分析器 —> 优化器 —> 权限校验 —> 执行器 —> 引擎
  - 更新 分析器 -> 权限校验 -> 执行器 —> 引擎 — > redo log prepare —> binlog —> redo log commit

