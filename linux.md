## free
  - `free  -h -s`
  - mem buffer swap
## crontab
  - 添加定时任务 `crontab -e`
  - 查看定时任务  `crontab -l`
  - 时间格式：分时日月周

## 查看文件命令
  - cat 小文件
  - more 可分页 但不可回看
  - less 
  - head
  - tail -f
## find
  - find / -name cwtap.log
  - name size ctime pem user
## grep 
  - e(多条件or)  v(取反)
## sed 行操作
 `sed -n '1p;5p' cwtap.log`
 `sed -n '1,5p' cwtap.log`
## awk 列操作
   - `awk -F ' ' '{print $1}' cwtap.log`
   - `cat $1|grep 'cwtapMiddleware 本次请求响应时间'|cut -c 56-72|awk '{sum+=$1} END {print "total request = " NR; print "request average = " sum/NR}'`

## 创建linux新用户操作
  - 创建用户（root用户下执行） `useradd user_name`
  - 设置用户密码 `passwd user_name`
  - 设置sudo操作权限 `/etc/sudoers`
  - 删除用户 `userdel -r user_name`
 <img width="667" alt="屏幕快照 2022-04-12 上午10 51 36" src="https://user-images.githubusercontent.com/40445471/162869848-4e798507-17bf-4886-ada6-ba7975d0d07c.png">
