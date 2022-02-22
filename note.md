## JWT认证
- 传统session存在的问题
  - sesison存储占用内存
  - 分布式服务限制了应用的拓展
  - 浏览器存储session产生泄露的风险
- JWT的构成
  第一部分我们称它为头部（header),第二部分我们称其为载荷（payload, 类似于飞机上承载的物品)，第三部分是签证（signature)
  - header
    jwt的头部承载两部分信息,然后将头部进行base64加密（该加密是可以对称解密的),构成了第一部分.
    - 声明类型，这里是jwt
    - 声明加密的算法 通常直接使用 HMAC SHA256
  - playload
    载荷就是存放有效信息的地方。这些有效信息包含三个部分
    - 标准中注册的声明
    - 公共的声明 
    - 私有的声明
  - signature
    jwt的第三部分是一个签证信息，这个签证信息由三部分组成：
    - header (base64后的)
    - payload (base64后的)
    - secret
