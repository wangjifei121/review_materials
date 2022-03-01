### MySql存储引擎种类
- 可通过`SHOW ENGINES;`查看mysql支持的存储引擎,总计支持9种，其中常见的为`MyISAM`和`InnoDB`两种

```
mysql> SHOW ENGINES;
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| Engine             | Support | Comment                                                        | Transactions | XA   | Savepoints |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| ARCHIVE            | YES     | Archive storage engine                                         | NO           | NO   | NO         |
| BLACKHOLE          | YES     | /dev/null storage engine (anything you write to it disappears) | NO           | NO   | NO         |
| MRG_MYISAM         | YES     | Collection of identical MyISAM tables                          | NO           | NO   | NO         |
| FEDERATED          | NO      | Federated MySQL storage engine                                 | NULL         | NULL | NULL       |
| MyISAM             | YES     | MyISAM storage engine                                          | NO           | NO   | NO         |
| PERFORMANCE_SCHEMA | YES     | Performance Schema                                             | NO           | NO   | NO         |
| InnoDB             | DEFAULT | Supports transactions, row-level locking, and foreign keys     | YES          | YES  | YES        |
| MEMORY             | YES     | Hash based, stored in memory, useful for temporary tables      | NO           | NO   | NO         |
| CSV                | YES     | CSV storage engine                                             | NO           | NO   | NO         |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
9 rows in set (0.01 sec)

mysql> 
```
在MySQL中，不需要在整个服务器中使用同一种存储引擎，针对具体的要求，可以对每一个表使用不同的存储引擎。
Support列的值表示某种引擎是否能使用：YES表示可以使用、NO表示不能使用、DEFAULT表示该引擎为当前默认的存储引擎 。下面来看一下其中几种常用的引擎。

- InnoDB存储引擎

1. 支持ACID的事务，支持事务的四种隔离级别
2. 支持行级锁及外键约束：因此可以支持写并发
3. 不存储总行数
4. 一个InnoDb引擎存储在一个文件空间（共享表空间，表大小不受操作系统控制，一个表可能分布在多个文件里），也有可能为多个（设置为独立表空，表大小受操作系统文件大小限制，一般为2G），受操作系统文件大小的限制；
5. 引采用聚集索引（索引的数据域存储数据文件本身），辅索引的数据域存储主键的值；因此从辅索引查找数据，需要先通过辅索引找到主键值，再访问辅索引；最好使用自增主键，防止插入数据时，为维持B+树结构，文件的大调整。

- MyISAM存储引擎

1. 不支持事务，但是每次查询都是原子的
2. 支持表级锁，即每次操作是对整个表加锁
3. 存储表的总行数
4. YISAM表有三个文件：索引文件、表结构文件、数据文件
5. 聚集索引，索引文件的数据域存储指向数据文件的指针。辅索引与主索引基本一致，但是辅索引不用保证唯一性。

### Mysql中InnoDB支持的四种事务隔离级别 https://zhuanlan.zhihu.com/p/117476959/

- 事务的并发问题
    - 脏读：事务A读取了事务B更新的数据，然后B回滚操作，那么A读取到的数据是脏数据
    - 不可重复读：事务 A 多次读取同一数据，事务 B 在事务A多次读取的过程中，对数据作了更新并提交，导致事务A多次读取同一数据时，结果 不一致。
    - 幻读：系统管理员A将数据库中所有学生的成绩从具体分数改为ABCDE等级，但是系统管理员B就在这个时候插入了一条具体分数的记录，当系统管理员A改结束后发现还有一条记录没有改过来，就好像发生了幻觉一样，这就叫幻读。

    小结：不可重复读的和幻读很容易混淆，不可重复读侧重于修改，幻读侧重于新增或删除。解决不可重复读的问题只需锁住满足条件的行，解决幻读需要锁表

- MySQL事务隔离级别
    - 读未提交（READ UNCOMMITTED）
    - 读提交 （READ COMMITTED）
    - 可重复读 （REPEATABLE READ）,InnoDB默认隔离级别
    - 串行化 （SERIALIZABLE）

    读未提交和串行化基本上是不需要考虑的隔离级别，前者不加锁限制，后者相当于单线程执行，效率太差。
    可重复读的隔离级别下使用了MVCC机制，select操作不会更新版本号，是快照读（历史版本）；insert、update和delete会更新版本号，是当前读（当前版本）。
    可重复读级别解决了幻读问题，是通过行锁和间隙锁的组合 Next-Key 锁实现的。https://blog.csdn.net/bigtree_3721/article/details/73731377

- 可通过`show variables like 'transaction_isolation';`或`SELECT @@transaction_isolation`查看数据库隔离级别

```
mysql> show variables like 'transaction_isolation';
+-----------------------+-----------------+
| Variable_name         | Value           |
+-----------------------+-----------------+
| transaction_isolation | REPEATABLE-READ |
+-----------------------+-----------------+
1 row in set (0.00 sec)

mysql> 
mysql> 
mysql> SELECT @@transaction_isolation
    -> ;
+-------------------------+
| @@transaction_isolation |
+-------------------------+
| REPEATABLE-READ         |
+-------------------------+
1 row in set (0.00 sec)

mysql> 
```
### MySQL中varchar与char的区别以及varchar(50)中的50代表的涵义
    - varchar与char的区别 char是一种固定长度的类型，varchar则是一种可变长度的类型  
    - varchar(50)中50的涵义 最多存放50个字符，varchar(50)和(200)存储hello所占空间一样，但后者在排序时会消耗更多内存，因为order by col采用fixed_length计算col长度(memory引擎也一样) 

### Mysql日志文件种类
- 错误日志(error log)
    查看错误日志 `show variables like 'log_error';`，默认情况下以服务器的主机名命名`hostname`.err，可以通过参数--log-error=[file_name]指定
    ```
    mysql> show variables like 'log_error';
    +---------------+---------------------+
    | Variable_name | Value               |
    +---------------+---------------------+
    | log_error     | /var/log/mysqld.log |
    +---------------+---------------------+
    1 row in set (0.07 sec)

    mysql> 
    mysql> ps -ef|grep mysql
    mysql    11005  0.0  0.7 3477144 470428 ?      Sl    2020 319:54 /usr/local/mysql/bin/mysqld --basedir=/usr/local/mysql --datadir=/var/lib/mysql --plugin-dir=/usr/local/mysql/lib/plugin --user=mysql --log-error=/var/log/mysqld.log --pid-file=/var/lib/mysql/server348.pid --socket=/var/lib/mysql/mysql.sock
    mysql> 
    ```
- 查询日志(general log)
    查询日志分为一般查询日志和慢查询日志，通过参数long_query_time指定时间的值对其进行判定，如果在参数设定时间内完成查询，则为一般查询日志（建议关闭，因为太多），否则为慢查询日志。
- 慢查询日志日志(slow query log)
    查询超出变量 long_query_time 指定时间值的为慢查询。mysql记录慢查询日志是在查询执行完毕且已经完全释放锁之后才记录的，因此慢查询日志记录的顺序和执行的SQL查询语句顺序可能会不一致
    查看慢查询日志：`show variables like '%slow_query_log%';`
    
    开启慢查询方式：
    ```
    # 方式一：配置文件设置
    [mysqld]
    slow_query_log=ON # 是否开启慢查询
    slow_query_log_file=/usr/local/mysql/data/slow.log     # 指定慢查询日志路径
    long_query_time=1 # 慢查询判定时间
    
    # 方式二：全局变量设置
    mysql> set global slow_query_log='ON'; # 是否开启慢查询
    mysql> set global slow_query_log_file='/usr/local/mysql/data/slow.log'; # 指定慢查询日志路径
    mysql> set global long_query_time=1; # 慢查询判定时间
    ```
- 二进制日志(binlog)
    记录对mysql数据库执行了更改的所有操作，不包括select和show这样的操作，如果执行了update和delete这样的操作，但是没有引起数据库数据的任何变化，也可能被写入二进制日志文件中。
    - 二进制文件的开启
        默认情况下不开启二进制日志，开启时需要修改my.ini配置文件
        ```
        [mysqld]
        bog-bin=/usr/local/mysql/data/bin.log # 指定二进制日志路径
        ```
    - 二进制日志的作用
        1. 恢复：用户可以通过二进制文件的point-in-time进行恢复
        2. 复制：通过执行二进制的文件在远程的机器上恢复数据
        3. 审计：可以对二进制日志文件进行审计，判断是否有对数据库进行注入攻击

### innodb事务日志
    nnodb事务日志包括redo log和undo log。redo log是重做日志，提供前滚操作，undo log是回滚日志，提供回滚操作。
### 数据库设计三大范式
   - 第一范式是最基本的范式。如果数据库表中的所有字段值都是不可分解的原子值，就说明该数据库表满足了第一范式
   - 第二范式在第一范式的基础之上更进一层。第二范式需要确保数据库表中的每一列都和主键相关，而不能只与主键的某一部分相关（主要针对联合主键而言）。也就是说在一个数据库表中，一个表中只能保存一种数据，不可以把多种数据保存在同一张数据库表中。
   - 第三范式需要确保数据表中的每一列数据都和主键直接相关，而不能间接相关
### sql执行顺序
    - `select distinct s.id  from T t join  S s on t.id=s.id where t.name="Yrion" group by t.mobile having count(*)>2  order by s.create_time limit`
![image](https://user-images.githubusercontent.com/40445471/155533725-9a9f18dd-a3ae-4083-a295-de4b8e92a7c2.png)
### mysql整体的执行过程
![image](https://user-images.githubusercontent.com/40445471/155534029-3825631f-91d0-4146-a088-42cf522ddb29.png)

### Btree和B+tree数据结构图示
 - Btree的构建过程图示
![image](https://user-images.githubusercontent.com/40445471/156132614-72465612-d9bd-48f5-ac30-6cc2e43b6f78.png)

![image](https://user-images.githubusercontent.com/40445471/156137646-e9f0e959-427f-401d-b9dc-96bd521e584b.png)

 - B+tree数据结构图示
    
![image](https://user-images.githubusercontent.com/40445471/156137536-03550374-1da8-4135-8a66-4ae7df9ea78e.png)
 - Btree和B+tree的区别
    ```
    - B+ 树非叶子节点上是不存储数据的，仅存储键值，而 B 树节点中不仅存储键值，也会存储数据。
        之所以这么做是因为在数据库中页的大小是固定的，InnoDB 中页的默认大小是 16KB。
        如果不存储数据，那么就会存储更多的键值，相应的树的阶数（节点的子节点树）就会更大，树就会更矮更胖，
        如此一来我们查找数据进行磁盘的 IO 次数又会再次减少，数据查询的效率也会更快。
    - 因为 B+ 树索引的所有数据均存储在叶子节点，而且数据是按照顺序排列的。
    ```
