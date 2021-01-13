1.目的
尝试借鉴 imagenet 的标签体系构建和标注过程，对 小说项目的 小说文本部分的 wordTree 构建 有思路启发，希望可以借鉴过来。
2. 先说结论
3. 总结imagenet中的构建
标签体系的构建
标注过程
4. ImageNet标签体系的构建
4.1  ImageNet vs. WordNet
wordnet
synset:  一个同义词集合 (若干个词组成，共同构成或者指向了一个概念语义，概念是基元不可再分，即一个 synset 唯一表示了一个概念)
根据词性，分为多个组各自分别形成一个语义网：名词，动词，形容词和副词
如果说WordNet是一个数据库，那么Synset就是一条数据的主键，而每一条数据，代表的是一个词义。Synset由三部分组成，第一部分是词义，第二部分是词性，第三部分是编。
WordNet的描述对象包含compound（复合词）、phrasal verb（短语动词）、collocation（搭配词）、idiomatic phrase（成语）、word（单词），其中word是最基本的单位。
WordNet不只是用同义词集合的方式罗列概念，而是把这些同义词集合用一定的关系类型关联起来的。其中有同义关系(synonymy)、反义关系(antonymy)、上下位关系(hypernymy/hyponymy)、整体和部分关系(meronymy)和继承关系(entailment)等。WordNet尽可能使词义之间的关系简单，使用起来方便。
上下位关系（动词、名词）、蕴含关系（动词）、相似关系（名词）、成员部分关系（名词）、物质部分关系（名词）、部件部分关系（名词）、致使关系（动词）、相关动词关系（动词）、属性关系（形容词）。
在WordNet中，大多数的同义词集都有说明性的注释，但一个Synset不等于词典中的一个词条，因为一个Synset只包含一个注释，而在传统词典中的词条是多义词，会有多个解释。
一个Synset等于的是一个词义 这一点必须反复强调。以一条词义为一条数据，是跨语言想要成立所必须的条件。
WordNet Hierarchy: TODO, 太偏自然语言，暂时没空
基本操作，可借助python接口: [4]
imagenet
1) ImageNet currently only considers nouns, ImageNet is based upon WordNet 3.0，取其中全部的名词性的 synsets (~80k, 每个synset 配 500~1000张图片). 全部的 synsets的 WordNet ID 见 [7][8][9].   (12 subtrees with5247 synsets and 3.2 million images in total. )
2) 自顶向下的目录树结构(仅显示一级结构，还有更多级的细划分)，参考 [10][11]


[13], 哺乳动物->胎生动物->食肉动物->犬类->狗->工作犬->哈士奇
3) 综上，上述 标签体系还是继承 WordNet, 而 WordNet 是 基于认知语言学 对语言的 同义词为基元 构建字典，所以还是有很多专家知识的，如果想 follow, 体系可以模仿，但是专家知识无法规避 (但可以借鉴 类似WordNet 这种 专家知识嘛，无须自己重新构建地基)
ISLVRC 2012 fall
本质是：单标签多分类 (类别这1个标签，有1000种选择)，为了更好组织理解1000类的关系，将这1000类组织为多级决策树，step-by-step 从根节点直至到达 叶子节点；最困难的是 多标签多分类
层次结构: 若干个synsets -> 若干级细分 -> 1000 类 -> 每类1000张图片(每类的1000张图片放在一个文件夹下)，共计 100w 张图像
标注过程的直观感受呢？应该有一颗决策树(每个节点属性处应该是二分选择？)，step-by-step (就是点击一个按钮即确定了当前的这一级的某个大分类选啥，然后继续选择下一级选啥) 告诉标注人员，当前这张图片 应该标注为什么？不可能让标注员做 1000选1 的标记；
举个 imagenet的例子：

[13], 哺乳动物->胎生动物->食肉动物->犬类->狗->工作犬->哈士奇

[13], 哺乳动物下面有1180个子类，而最高频的是 人类
再举个 多标签多分类 的 例子:

[12], 举个其他的 多标签多分类的 多级标注的 流程图

[12], 复杂版，但是更多的属性，在logic 上等价于上面第一个简化版，所以只需要重复操作即可
一些易错点辨析
imagenet的变化 (一般用的 2011 版，而竞赛用的是 ISLVRC2012 fall 使用的子集)
List of all image URLs of Fall 2011 Release
List of all image URLs of Winter 2011 Release
List of all image URLs of Spring 2010 Release
List of all image URLs of Fall 2009 Release
ImageNet vs. ISLVRC
参考
[1]. 知识图谱之WordNet
[2]. 安立桐：【Python&NLP】关于WordNet，我的一些用法和思路（一）
[3]. 安立桐：【Python&NLP】关于WordNet，我的一些用法和思路（二）
[4]. WordNet Interface
[5]. mapping_imagenet-wordnet
[6]. WordNet Documentation
[7]. http://www.image-net.org/api/text/imagenet.synset.obtain_synset_list (ImageNet中全部的 synset，用 WordNet ID 表示)
[8]. http://www.image-net.org/archive/words.txt (WordNet ID 与 word 的mapping file)
[9]. http://www.image-net.org/archive/gloss.txt (WordNet ID 与 对应的word的详细注解 的 mapping file)
[10]. ImageNet Tree View (ImageNet的结构树, 图示版)
[11]. http://www.image-net.org/api/xml/structure_released.xml (ImageNet的结构树, xml文件版, 这个比 图示版 更容易总结 tree, 因为可以看到每个概念synset的语义注解；而图示版适合直观看下每个节点下的图片)
[12]. 用户画像标签体系--从零开始搭建实时用户画像(三)
[13]. http://www.image-net.org/papers/ImageNet_2010.ppt (很有insight, 建议阅读)

5. 如何设计好的标注过程？
challenge: 如何加速标注速度 ?

[13], 对标注时间的封顶估计，待标注40k类，每类须覆盖10k张图片，每张图片都需要平均3个人独立标注并投票；引入众包后，N个人并行标注
Two Step
算法/人工 方法获得 1000类对应的候选集
基于wordTree得到的最终1000类的叶子节点的名词，作为 key word 去搜索引擎中搜索图片并下载，收集的图片作为候选集，最终形成 1000类x10000张的 image candidate
通过人工check logic发现 acc = 10% (即 搜索引擎的只有10%的靠谱度，目标后续人工修正，使得acc达到90%甚至是100%)
人工标注/修正原始图片的标签
基于总包平台(Amazon  Mechanical  Turk  (AMT))，以类为组，分别处理1000类中的每个类
对于某个类，让标注员 check它候选集中的10000张图片，挑选哪1000张 最应该属于这一类？ (当然，10000张图片分为 1000页，每页只展示10张图片，询问某个标注员，当前10张图片 有哪几张属于 这个类？至少选1张)；最后10000张确保要召回1000张，如果确实召回不了，就继续扩充候选集
如何挑选候选集
多搜索引擎即多源: google, badiu, biying, yahoo
多关键词：1)确定初始源，一颗wordTree, root->1000个类(叶子节点), 即1000个 query_word list；2) 同义词近义词，2) 多个同义词组合，比如 imagenet 就是 核心主要词+gloss中出现的辅助词；比如 帅气->帅气的人/男孩/男人/帅哥
多语言: 将 query word 翻译为多个语言，收集不同语言下的图像库
类间图片去重，得到 1000类型*10000张图片 (当然，还有一些 图像预处理操作，比如 resize, enhancement)
如何 人工标注 candidate set
总体流程
for Ci in C_1000_list:
	# 询问标注员，从当前类的 10000张候选图片集中 选择1000张 作为这个类的最终图片集
  #
  # 我猜想的可能的细节 (原论文没提)
  # (1) 将10000张分为 1000页，每页10张图片
  # (2) 对于某个标注员，给一页的10张图片，让他挑选，哪几张 属于当前类？(至少选1张？)

 关键点-1：确保标注员 理解了 当前类的含义
给 文字版的 defination (辅助理解)
给 图片样例 (辅助理解)
给 百度链接，可以一键点开百度百科，看 文字/图片
设置 quiz, 标注前必须独立完成 quiz 达到分数阈值，才能开始标注
关键点-2：使用投票机制减少单个标注意见的bais
多个人对一张图像 独立标注 yes/no，如果 yes 的意见一致，那么接收这张图像的标注结果为 yes, 否则系统标注为 hard-case, 送入下一轮 继续标注 或者 算法员 单独拿出来 分析
一个核心问题是：共识度阈值，对于不同类，是不同的，需要根据当前类的 hard case 难易程度来确定，这个小算法还没看懂，原文没细讲，找不到更多资料
我的启发: 
ImageNet的标注过程非常有启发性，对于 多标签多分类任务 非常有用，如果能将标注任务转化为 单标签多分类，可以 follow这个过程
全局参考
[1]. 量子位：ImageNet这八年：李飞飞和她改变的AI世界  
[2]. http://www.image-net.org/about-cool-stuff (feifei li 博客下对 imagenet的使用)
[3]. http://image-net.org/update-sep-17-2019 (imagenet 最新的改进)
[4]. ImageNet数据集到底长什么样子？
[5]. 深度学习与计算机视觉(PB-13)—ImageNet数据集准备 (一个不错的实践)
[6]. http://www.image-net.org/explore_cloud.php (特别好的一个可视化 数据分布规律 的方式，学习它的代码)
[7]. 用户画像标签体系--从零开始搭建实时用户画像(三) (非常有启发性)

