# elasticsearch复习资料
## 一、es概念性问题
### elasticsearch 的倒排索引是什么
而倒排索引，是通过分词策略，形成了词和文章的映射关系表，这种词典+映射表即为倒排索引

倒排索引的底层实现是基于：FST（Finite State Transducer）数据结构。
lucene 从 4+版本后开始大量使用的数据结构是 FST。FST 有两个优点：
- 1、空间占用小。通过对词典中单词前缀和后缀的重复利用，压缩了存储空间；
- 2、查询速度快。O(len(str))的查询时间复杂度。

![屏幕快照 2022-02-04 下午3 55 36](https://user-images.githubusercontent.com/40445471/152492366-1e0ec5a1-77cd-4a99-a473-d23fee31f2b3.png)
