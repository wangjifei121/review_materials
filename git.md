## git命令总览
![image](https://user-images.githubusercontent.com/40445471/163094002-493e19cc-97dd-4867-87b4-98a8bf17758f.png)
## git工作流程
![image](https://user-images.githubusercontent.com/40445471/163094063-7dd0fd2e-0562-4088-ae89-22ec9e0b7ec9.png)
## git指定分支拉取代码
`git clone -b dev <url>`
## 在mac中配置多个git账号
- 应用场景
  本地需要将不同代码管理在github、gitlab等不同的仓库中
- 操作步骤总览
  ```
  取消全局配置（若之前全局配置过则需要取消全局配置，否则可跳过）
  对每个账户生成各自的秘钥
  将私钥添加到本地
  对本地秘钥进行配置
  将公钥添加到托管网站
  使用
  ```
- 具体操作
  - 取消全局配置
    - 若已经全局配置过Git (即曾经执行过如下命令)
     ```
      git config --global user.name "xxx" // 配置全局用户名，如Github上注册的用户名
      git config --global user.email "xxx@xx.com" // 配置全局邮箱，如Github上配置的邮箱
     ```
      这里的 --global 指全局配置 user.name 和 user.email ，即不同的Git仓库默认的用户名和邮箱都是这个值。
      由于需要管理多个账户，所以仅使用全局值是不合适的，需要针对每个仓库单独配置。

    - 查看是否已经配置过：
      ```
      (smartdot) (base) bogon:.ssh wangjifei$ git config --global user.name
      wangjifei
      (smartdot) (base) bogon:.ssh wangjifei$ git config --global user.email
      18500327026@163.com
      (smartdot) (base) bogon:.ssh wangjifei$ 
      ```
     - 如果之前已经配置过，则使用如下命令清除：
     ```
      (smartdot) (base) bogon:.ssh wangjifei$ git config --global --unset user.name
      (smartdot) (base) bogon:.ssh wangjifei$ 
      (smartdot) (base) bogon:.ssh wangjifei$ git config --global --unset user.email
      (smartdot) (base) bogon:.ssh wangjifei$
     ```
  - 生成密钥
    每个git账户对应一对密钥
     ```
     (smartdot) (base) bogon:.ssh wangjifei$ cd ~/.ssh
     (smartdot) (base) bogon:.ssh wangjifei$ ssh-keygen -t rsa -C "18500327026@163.com"
     Generating public/private rsa key pair.
     Enter file in which to save the key (/Users/wangjifei/.ssh/id_rsa): id_rsa_github
     ```
     如上提示表示可对生成的秘钥文件进行重命名，默认为 id_rsa 。
     由于要配置多个账户，在此需要重命名以区分。例如：重命名为 id_rsa_github 。
     设置密码可以直接按回车，直到秘钥生成。
     在.ssh秘钥目录下可以看到两个文件 id_rsa_github 和 id_rsa_github.pub。
     对于另外的gitLab 的账户，采用相同的步骤进行生成秘钥 id_rsa_gitlab 
     设置成功会显示如下：
     ```
      Your identification has been saved in id_rsa_github.
      Your public key has been saved in id_rsa_github.pub.
      The key fingerprint is:
      SHA256:SGK8Gx7MeSrpMGQy4NAkBTXfZnIlLbdN+3v5jSA43Eo 18500327026@163.com
      The key's randomart image is:
      +---[RSA 2048]----+
      |o+=   ...        |
      | + + ..oo .      |
      |o . * *o + .     |
      |+  + X .. o      |
      |o+  B o S  .     |
      |+. o * . o  .    |
      |o o +   E o .. . |
      | + .   . o ...o..|
      |  .     .    ...o|
      +----[SHA256]-----+
      (smartdot) (base) bogon:.ssh wangjifei$ 
     ```
 
 - 将私钥添加到本地
    ```
    ssh-add ~/.ssh/id_rsa_github // 将GitHub私钥添加到本地
    ssh-add ~/.ssh/id_rsa_gitlab // 将GitLab私钥添加到本地
    ```
    检验本地是否添加成功
    ```
    (smartdot) (base) bogon:.ssh wangjifei$ ssh-add -l
    2048 SHA256:SGK8Gx7MeSrpMGQy4NAkBTXfZnIlLbdN+3v5jSA43Eo 18500327026@163.com (RSA)
    2048 SHA256:t+wdMML/u3XddxGwO0Vc5YkbInJwVmv/uSPgrGLiJ5Y 18516987026@163.com (RSA)
    ```
  - 对本地秘钥进行配置
    由于添加了多个密钥文件，所以需要对这些密钥进行管理
    - 在.ssh目录下新建一个config文件
       ```
       touch config
       ```
   - 将文件内容添加到config文件中
   ```
    Host github // 网站的别名，自己取
    HostName github.com // 托管网站的域名
    User wangjifei121 // 托管网站上的用户名
    IdentityFile ~/.ssh/id_rsa_github  // 使用的密钥文件

    Host gitlab
    HostName http://172.20.90.93/
    User wangjifei 
    IdentityFile ~/.ssh/id_rsa_gitlab
    Port 80 // 可选，端口可能被禁用，若提示端口被禁需要使用其他端口
   ```
 - 将公钥添加到托管网站
  ```
  vim id_rsa_gitlab.pub
  ```
   
   
   
   
   
   
   
   
   
   
   
