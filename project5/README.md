**Project5: Impl Merkle Tree following RFC6962**

**实验要求**

• Construct a Merkle tree with 10w leaf nodes

• Build inclusion proof for specified element

• Build exclusion proof for specified element

**背景知识**

Merkle树是一种哈希树的数据结构，用于验证和确保大型数据集中的数据的完整性。它是由计算机科学家Ralph Merkle在1979年首次提出的。RFC6962定义了一种特定类型的Merkle树，称为"Certificate Transparency"（CT）Merkle树。
RFC6962旨在解决数字证书领域中的安全问题，例如SSL/TLS证书的伪造和滥用。CT Merkle树通过将数字证书存储在一个可公开和公证的日志中来增强证书的透明度和可验证性。

**CT Merkle树的构建遵循以下步骤：**

将每个数字证书计算为其哈希值（通常使用SHA-256算法）。

将这些证书哈希值按顺序排列，组成叶节点列表。

如果叶节点数目是奇数，则复制最后一个叶节点并添加到列表末尾以确保树的完整性。

逐对对叶节点进行哈希操作，生成新的哈希值作为父节点。如果有奇数个节点，则最后一个节点不需要兄弟节点，直接作为父节点。

重复以上步骤，直到最终只剩下一个根节点，即Merkle树的根哈希。

**CT Merkle树具有以下特点和优势：**

完整性验证：通过比较存储在根哈希中的哈希值与日志中的数据哈希值，可以验证数据的完整性。如果根哈希匹配，则可以确定所有证书都未被篡改。

高效验证：由于Merkle树是一种二叉树，所以只需存储根哈希值即可验证整个数据集，而不需要存储所有原始数据。

可验证性和透明度：由于CT Merkle树是公开和公证的，任何人都可以验证证书是否存在于日志中，增加了数字证书系统的透明度。

抵抗篡改：如果有人试图更改或删除日志中的任何证书，Merkle树的结构将发生变化，从而轻松检测到潜在的攻击行为。

**代码思路：**

首先，定义hash_leaf(data)函数，用于计算给定数据的哈希值，使用SHA-256算法对数据进行哈希，并返回结果。

接下来，build_merkle_tree(leaves)函数用于构建Merkle树，接受一个叶节点列表作为输入，然后递归地将叶节点对进行哈希操作，生成新的父节点，最终得到Merkle树的根节点。如果叶节点数目为奇数，它会复制最后一个叶节点并添加到列表末尾以确保树的完整性。

calculate_merkle_root(leaves)函数调用build_merkle_tree()函数构建Merkle树，并返回根节点的哈希值，即Merkle树的根哈希。

get_proof(index, leaves)函数用于生成给定叶节点索引的证明。它通过向上遍历Merkle树的路径，记录与当前叶节点相邻的兄弟节点的哈希值，生成证明列表。该证明列表可以用于验证特定叶节点是否属于Merkle树。

**运行结果**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/8f420191-c85f-43ea-9fac-06dd94b259fa)

