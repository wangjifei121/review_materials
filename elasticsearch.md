# elasticsearch复习资料
## 一、es概念性问题
### elasticsearch 的倒排索引是什么
倒排索引，是通过分词策略，形成了词和文章的映射关系表，这种词典+映射表即为倒排索引

倒排索引的底层实现是基于：FST（Finite State Transducer）数据结构。
lucene 从 4+版本后开始大量使用的数据结构是 FST。FST 有两个优点：
- 1、空间占用小。通过对词典中单词前缀和后缀的重复利用，压缩了存储空间；
- 2、查询速度快。O(len(str))的查询时间复杂度。

![屏幕快照 2022-02-04 下午3 55 36](https://user-images.githubusercontent.com/40445471/152492366-1e0ec5a1-77cd-4a99-a473-d23fee31f2b3.png)

### elasticsearch是如何实现master选举的
master选举的三条规则
- 对所有可以成为master的节点根据nodeId排序，每次选举每个节点都把自己所知道节点排一次序，然后选出第一个（第0位）节点，暂且认为它是master节点。
- 如果对某个节点的投票数达到一定的值（可以成为master节点数n/2+1）并且该节点自己也选举自己，那这个节点就是master。否则重新选举。
- 对于脑裂问题，需要把候选master节点最小值设置为可以成为master节点数n/2+1（quorum ）

### es分片及分片使用
ES中所有数据均衡的存储在集群中各个节点的分片中，会影响ES的性能、安全和稳定性。
简单来讲就是咱们在ES中所有数据的文件块，也是数据的最小单元块，整个ES集群的核心就是对所有分片的分布、索引、负载、路由等达到惊人的速度

分片的作用：
  - 允许你水平分割/扩展你的内容容量。 
  - 允许你在分片之上进行分布式的、并行的操作，进而提高性能/吞吐量

分片设置一般原则：
   - 每一个分片数据文件小于30GB
   - 每一个索引中的一个分片对应一个节点
   - 节点数大于等于分片数

### match、match_phrase和match_phrase_prefix的区别
- match：用于执行全文查询的标准查询，包括模糊匹配和短语或接近查询。重要参数：控制Token之间的布尔关系：operator：or/and
- match_phrase：与match查询类似，但用于匹配确切的短语或单词接近匹配。重要参数：Token之间的位置距离：slop 参数
- match_phrase_prefix：与match_phrase查询类似，但是会对最后一个Token在倒排序索引列表中进行通配符搜索。重要参数：模糊匹配数控制：max_expansions 默认值50，最小值为1
