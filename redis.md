
### redis数据结构及常用场景
  redis主要的数据结构包括 string、list、hash、set、 zset五种
  - string类型
    - 缓存功能：String字符串是最常用的数据类型，不仅仅是Redis，各个语言都是最基本类型，因此，利用Redis作为缓存，配合其它数据库作为存储层。
    - 计数器：许多系统都会使用Redis作为系统的实时计数器，可以快速实现计数和查询的功能。而且最终的数据结果可以按照特定的时间落地到数据库或者其它存储介质当中进行永久保存。
    - 共享用户Session
  - list类型
    - 消息队列：Redis的链表结构，可以轻松实现阻塞队列，可以使用左进右出的命令组成来完成队列的设计
    - 列表数据或者数据分页展示的应用
  - hash类型
    - 分组数据的存储
    - 各种复杂的字典结构数据缓存
  - set类型
    - 可借助集合操作的业务数据（去重、集合运算）
  - zset类型
    - 各种排行榜相关业务

 ### redis数据持久化
  Redis 提供了 RDB 和 AOF 两种持久化方式。RDB做镜像全量持久化，AOF做增量持久化。因为RDB会耗费较长时间，不够实时，在停机的时候会导致大量丢失数据，所以需要AOF来配合使用。在redis实例重启时，会使用RDB持久化文件重新构建内存，再使用AOF重放近期的操作指令来实现完整恢复重启之前的状态。
  
### redis缓存雪崩
  - 什么是缓存雪崩
    - 如果缓存服务器宕机，全部请求只能直接请求DB数据库
    - 如果缓存数据在同一时间点全部过期，导致全部请求只能直接请求DB数据库
  - 解决方案
    - 在缓存的时候给过期时间加上一个随机值，这样就会大幅度的减少缓存在同一时间过期
    - 缓存宕机情况的解决方案
      - 事发前：实现Redis的高可用(主从架构+Sentinel 或者Redis Cluster)，尽量避免Redis挂掉这种情况发生。
      - 事发中：万一Redis真的挂了，我们可以设置本地缓存(ehcache)+限流(hystrix)，尽量避免我们的数据库被干掉(起码能保证我们的服务还是能正常工作的)
      - 事发后：redis持久化，重启后自动从磁盘上加载数据，快速恢复缓存数据
  
 ### redis缓存穿透
  访问一个不存在的key，缓存不起作用，请求会穿透到DB，流量大时DB会挂掉。
  
  解决方案：
   - 对不存在的用户，在缓存中保存一个空对象进行标记，防止相同 ID 再次访问 DB。不过有时这个方法并不能很好解决问题，可能导致缓存中存储大量无用数据。
   - 使用 BloomFilter 过滤器，BloomFilter 的特点是存在性检测，如果 BloomFilter 中不存在，那么数据一定不存在；如果 BloomFilter 中存在，实际数据也有可能会不存在。非常适合解决这类的问题。

### redis缓存击穿
  访问一个存在的key，在缓存过期的一刻，同时有大量的请求，这些请求都会击穿到DB，造成瞬时DB请求量大、压力骤增
  
  解决方案
   - 设置热点数据永远不过期。
   - 加互斥锁

### BloomFilter 过滤器
- 和HyperLogLog超对数对比
  超对数包含pfadd、pfcount两个命令，但是无法判断一个已知元素在不在HyperLogLog中
- 什么是BloomFilter过滤器
  BloomFilter过滤器是一个很长的二进制向量和一系列随机映射函数。布隆过滤器可以用于检索一个元素是否在一个集合中。它的优点是空间效率和查询时间都远远超过一般的算法，缺点是有一定的误识别率和删除困难。
  BloomFilter过滤器时redis4.0版本以后增加的功能，默认不支持，需要添加插件才能适用
- BloomFilter过滤器适用场景
  - 大数据量
  - 不要求准确率100%
  - 需要查询元素是否已经存在
  - 应用场景举例：
    - 根据用户浏览记录给用户推荐内容
    - 爬虫url去重
    - 邮件垃圾箱
    - 挡IO，不存在时再查库
- BloomFilter过滤器常用命令
  ```
  bf.add key val
  bf.existes key val
  bf.madd key val1 val2
  bf.mexistes key val1 val2 val3
  ```
- BloomFilter的准确率
  - BloomFilter过滤器对已经见过的数据肯定不会误判，准确度100%
  - BloomFilter过滤器对未知的数据的准确度默认为99%，可以根据实际需求修改，准确度要求越高，占用空间越大
- 自定义设置BloomFilter的准确率
  - 命令 `bf.reserve`
  - 参数1 `key`
  - 参数2 `error_rate` 默认0.01
  - 参数3 `initial_size` 预计存在元素个数，如果实际数量超过预设数量，准确度会下降，默认值为100
- BloomFilter布隆过滤器图示
![image](https://user-images.githubusercontent.com/40445471/154433140-97311257-e9fe-46a8-ae74-a0d82fc7ba95.png)

### redis Geohash 基于地理位置
  - Redis在3.2版本后增加了地理位置GEO模块， 意味着可以使用Redis来实现摩拜但这[附近的Mobike]、美团和饿了么[附近的餐馆]这样的功能了。
  - GeoHash算法：业界比较通用的地理位置距离排序算法时GeoHash算法， Redis也使用了GeoHash算法。 GeoHash算法将二维的经纬度数据映射到一维的整数， 这样所有的元素都将挂在到一条线上， 距离靠近的二维坐标映射到一维后的点之间距离也会很接近。 当我们想要计算[附近的人]， 首先将目标位置映射到这条线上， 然后在这个一维的线上获取附近的点就可以了
  - redis Geo命令
    - geoadd 添加数据
      
      ```
      127.0.0.1:6379> geoadd city 116.397128 39.916527 beijing
      (integer) 1
      127.0.0.1:6379> geoadd city 116.68572 39.50311 langfang
      (integer) 1
      127.0.0.1:6379> geoadd city 114.507132 37.06787 xingtai
      (integer) 1
      127.0.0.1:6379> geoadd city 116.75199 36.55358 jinan
      (integer) 1
      ```
      
     - geodist 计算两元素之间的距离，距离单位可以是m、km、ml、ft分别代表米、千米、英里和尺
        
        ```
        127.0.0.1:6379> geodist city beijing xingtai km
        "356.9957"
        127.0.0.1:6379> geodist city beijing langfang km
        "52.1934"
        ```
        
     - geopos 可以获取集合中任意元素的经纬度坐标，可以一次获取多个
          
          ```
          127.0.0.1:6379> geopos city beijing xingtai
          1) 1) "116.39712899923324585"
             2) "39.91652647362980844"
          2) 1) "114.50713187456130981"
             2) "37.06786995982209731"
          ```
          
      - geohash 可以获取元素的经纬度编码字符串， 上面提到， 它是base32编码。 可以使用这个编码值取http://geohash.org/${hash}中进行直接定位， 它是geohash的标准编码值
         
         ```
           127.0.0.1:6379> geohash city beijing
           1) "wx4g0dtf9e0"
           ```
           
      - georadiusbymember  它可以用来查询指定元素附近的其他元素
          
          ```
          # 查询北京附近200km范围内的前两个城市正序排列
          127.0.0.1:6379> georadiusbymember city beijing 200 km count 3 asc
          1) "beijing"
          2) "langfang"
          
          # 查询北京附近200km范围内的前两个城市倒序排列
          127.0.0.1:6379> georadiusbymember city beijing 200 km count 3 desc
          1) "langfang"
          2) "beijing"
          
          # 三个可选参数withcoord(经纬度) withdist(距离) withhash(hash值) 用来携带附加参数
          127.0.0.1:6379> georadiusbymember city beijing 200 km withcoord withdist withhash count 3 asc
          1) 1) "beijing"
             2) "0.0000"
             3) (integer) 4069885548668386
             4) 1) "116.39712899923324585"
                2) "39.91652647362980844"
          2) 1) "langfang"
             2) "52.1934"
             3) (integer) 4069137789659981
             4) 1) "116.6857185959815979"
                2) "39.50311091782047157"
          ```
      - georadius 根据坐标值来查询附近的元素
          
          ```
          # 查询某个位置坐标500km以内的城市top4，并输出具体举例
          127.0.0.1:6379> georadius city 117.07822 39.98246 500 km withdist count 4 asc
          1) 1) "beijing"
             2) "58.5358"
          2) 1) "langfang"
             2) "63.0035"
          3) 1) "jinan"
             2) "382.4432"
          4) 1) "xingtai"
             2) "393.8413"
          ```
