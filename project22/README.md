**Project22: research report on MPT**

**概述**

Merkle Patricia Tree是由Ralph C. Merkle和Patrick A. Duffin于1979年提出的一种哈希树结构，常用于快速验证和检索大量数据。MPT的设计旨在克服传统哈希树在存储和检索效率方面的一些限制。MPT在区块链技术中广泛应用，特别是以太坊等智能合约平台。

**作用**

存储任意长度的key-value键值对数据，符合以太坊的state模型；

提供了一种快速计算所维护数据集哈希标识的机制；

提供了快速状态回滚的机制；

提供了一种称为默克尔证明的证明方法，进行轻节点的扩展，实现简单支付验证；

**MPT的原理与结构**

MPT是一种基于前缀树（Trie）和默克尔树（Merkle Tree）的数据结构。它将键值对存储在树的叶子节点中，并使用键的前缀作为节点的索引。MPT通过哈希函数对节点进行哈希运算，确保树的完整性和安全性。MPT的主要特点是在保持数据完整性的同时，有效地支持数据的插入、删除和检索操作。

下面分别介绍一下前缀树（Trie）和默克尔树（Merkle Tree）

**前缀树（Trie）**

前缀树是一种用于高效存储和检索字符串的树形数据结构。它的设计基于字符串的共同前缀，将字符串按照字符逐级存储，从而实现快速的字符串匹配和搜索操作。

前缀树的主要特点是节点的关键字（字符）按照路径从根节点到叶子节点形成字符串的前缀。每个节点可以有多个子节点，每个子节点代表不同的字符。这种结构使得前缀树非常适合存储和搜索具有相同前缀的字符串集合。

![image](https://github.com/suibianchun/cxcysj/assets/138552183/498da4f8-0099-4326-a36c-39ae9ee9afb8)

上图是一棵Trie树，表示了关键字集合{“a”, “to”, “tea”, “ted”, “ten”, “i”, “in”, “inn”} 。

**默克尔树（Merkle Tree）**

默克尔树的主要特点是通过对数据进行哈希运算构建树结构。它将一组数据分成固定大小的块（通常为2的幂次），每个块通过哈希函数生成一个唯一的哈希值。然后，这些哈希值再逐级合并和哈希，直到最终形成一个根哈希值，称为根哈希（Root Hash）。

在默克尔树中，叶子节点存储着原始数据的哈希值，而非叶子节点存储着它的子节点的哈希值。每个非叶子节点的哈希值是由其子节点的哈希值计算得出的。这样的结构可以有效地检测数据的完整性。

通过根哈希，可以验证整个数据集的完整性。如果数据集中的任何一个块发生变化，将会导致根哈希的不同。因此，通过比较根哈希值，可以快速检测到数据是否被篡改或损坏。

下图是Merkle Tree的一个例子结构：
![image](https://github.com/suibianchun/cxcysj/assets/138552183/3683fe1d-dd29-4e8d-adce-0021e8d1ad0a)

**Merkle Patricia Tree**

MPT树结合了字典树和默克尔树的优点，在压缩字典树中根节点是空的，而MPT树可以在根节点保存整棵树的哈希校验和，而校验和的生成则是采用了和默克尔树生成一致的方式。 以太坊采用MPT树来保存，交易，交易的收据以及世界状态，为了压缩整体的树高，降低操作的复杂度，以太坊又对MPT树进行了一些优化。将树节点分成了四种：

空节点（hashNode）

叶子节点（valueNode）

分支节点（fullNode）

扩展节点（shortNode）

**结构图**
![image](https://github.com/suibianchun/cxcysj/assets/138552183/fd3d7658-57c3-4a63-9919-d69df856f616)

**对Merkle Patricia Tree的操作**

**更新**

函数_update_and_delete_storage(self, node, key, value)

i. 如果node是空节点，直接返回[pack_nibbles(with_terminator(key)), value]，即对key加上终止符，然后进行HP编码。
![image](https://github.com/suibianchun/cxcysj/assets/138552183/1c3121e3-0089-43c2-bcbf-77b0ae85b872)

ii. 如果node是分支节点，如果key为空，则说明更新的是分支节点的value，直接将node[-1]设置成value就行了。如果key不为空，则递归更新以key[0]位置为根的子树，即沿着key往下找，即调用_update_and_delete_storage(self._decode_to_node(node[key[0]]), key[1:], value)。

![image](https://github.com/suibianchun/cxcysj/assets/138552183/0dfa5df1-80b3-43d7-81f6-b39870b39f34)

iii. 如果node是kv节点（叶子节点或者扩展节点），调用_update_kv_node(self, node, key, value)，见步骤iv

iv. curr_key是node的key，找到curr_key和key的最长公共前缀，长度为prefix_length。Key剩余的部分为remain_key，curr_key剩余的部分为remain_curr_key。

a) 如果remain_key==[]== remain_curr_key，即key和curr_key相等，那么如果node是叶子节点，直接返回[node[0], value]。如果node是扩展节点，那么递归更新node所链接的子节点，即调用_update_and_delete_storage(self._decode_to_node(node[1]), remain_key, value)

![image](https://github.com/suibianchun/cxcysj/assets/138552183/3096fb66-0ac8-4ffb-aac1-11b3c9b2a3de)

b) 如果remain_curr_key == []，即curr_key是key的一部分。如果node是扩展节点，递归更新node所链接的子节点，即调用_update_and_delete_storage(self._decode_to_node(node[1]), remain_key, value)；如果node是叶子节点，那么创建一个分支节点，分支节点的value是当前node的value，分支节点的remain_key[0]位置指向一个叶子节点，这个叶子节点是[pack_nibbles(with_terminator(remain_key[1:])), value]
![image](https://github.com/suibianchun/cxcysj/assets/138552183/9125d111-e4be-4fa2-9134-5b96dc3baa49)

c) 否则，创建一个分支节点。如果curr_key只剩下了一个字符，并且node是扩展节点，那么这个分支节点的remain_curr_key[0]的分支是node[1]，即存储node的value。否则，这个分支节点的remain_curr_key[0]的分支指向一个新的节点，这个新的节点的key是remain_curr_key[1:]的HP编码，value是node[1]。如果remain_key为空，那么新的分支节点的value是要参数中的value，否则，新的分支节点的remain_key[0]的分支指向一个新的节点，这个新的节点是[pack_nibbles(with_terminator(remain_key[1:])), value]

d) 如果key和curr_key有公共部分，为公共部分创建一个扩展节点，此扩展节点的value链接到上面步骤创建的新节点，返回这个扩展节点；否则直接返回上面步骤创建的新节点

![image](https://github.com/suibianchun/cxcysj/assets/138552183/a7b34585-d007-467f-a6a2-4fcab6c6ddef)

v. 删除老的node，返回新的node

**删除**

删除的过程和更新的过程类似，函数名：_delete_and_delete_storage(self, key)

i. 如果node为空节点，直接返回空节点

ii. 如果node为分支节点。如果key为空，表示删除分支节点的值，直接另node[-1]=‘’, 返回node的正规化的结果。如果key不为空，递归查找node的子节点，然后删除对应的value，即调用self._delete_and_delete_storage(self._decode_to_node(node[key[0]]), key[1:])。返回新节点

iii. 如果node为kv节点，curr_key是当前node的key。

a) 如果key不是以curr_key开头，说明key不在node为根的子树内，直接返回node。

b) 否则，如果node是叶节点，返回BLANK_NODE if key == curr_key else node。

c)如果node是扩展节点，递归删除node的子节点，即调用_delete_and_delete_storage(self._decode_to_node(node[1]), key[len(curr_key):])。如果新的子节点和node[-1]相等直接返回node。否则，如果新的子节点是kv节点，将curr_key与新子节点的可以串联当做key，新子节点的value当做vlaue，返回。如果新子节点是branch节点，node的value指向这个新子节点，返回。

**查找**

查找操作更简单，是一个递归查找的过程函数名为：_get(self, node, key)

i. 如果node是空节点，返回空节点

ii. 如果node是分支节点，如果key为空，返回分支节点的value；否则递归查找node的子节点，即调用_get(self._decode_to_node(node[key[0]]), key[1:])

iii. 如果node是叶子节点，返回node[1] if key == curr_key else ‘’

iv. 如果node是扩展节点，如果key以curr_key开头，递归查找node的子节点，即调用_get(self._decode_to_node(node[1]), key[len(curr_key):])；否则，说明key不在以node为根的子树里，返回空




**MPT的应用**

MPT在分布式账本和区块链技术中具有广泛的应用。它被用于存储和验证区块链中的交易记录、智能合约状态和账户余额等关键数据。MPT的高效存储和验证机制使其成为实现快速和可扩展区块链系统的重要组成部分。

下面介绍MPT几个具体的应用场景：

1、区块链中的交易存储：在区块链中，MPT被用于存储和验证交易数据。每个交易被存储在MPT中的叶子节点上，而每个区块的头部包含了整个MPT的根哈希。通过验证根哈希，可以确保整个区块中的交易数据的完整性，从而有效地保护交易的可信性和不可篡改性。

2、智能合约状态存储：智能合约平台（如以太坊）使用MPT来存储智能合约的状态。每个智能合约状态被存储在MPT的叶子节点上，而每个区块的状态根包含了整个MPT的根哈希。通过验证状态根哈希，可以确保智能合约状态的一致性和完整性，从而确保智能合约的正确执行。

3、账户余额和身份验证：在分布式账本中，MPT被用于存储账户余额和身份验证信息。每个账户的余额和身份信息被存储在MPT的叶子节点上，而账本的根哈希用于验证整个账户数据的完整性和一致性。这种方式可以实现高效的账户余额查询和身份验证，同时保护账户数据的安全性。

4、数据存储和共享：MPT也可以用于存储和共享其他类型的数据。例如，分布式存储系统可以使用MPT来管理数据块的索引和完整性验证。通过根哈希，可以快速验证整个数据集的完整性，并实现高效的数据存储和检索。
