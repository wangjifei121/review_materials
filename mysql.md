## Mysql面试题

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
