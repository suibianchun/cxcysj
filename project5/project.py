import hashlib
import math


def hash_leaf(data):
    return hashlib.sha256(data).digest()


def build_merkle_tree(leaves):
    if len(leaves) == 0:
        return None
    if len(leaves) == 1:
        return leaves[0]

    tree = []
    # 如果叶节点数目为奇数，则复制最后一个叶节点，并添加到列表末尾
    if len(leaves) % 2 == 1:
        leaves.append(leaves[-1])

    for i in range(0, len(leaves), 2):
        left = leaves[i]
        right = leaves[i + 1]
        node_hash = hashlib.sha256(left + right).digest()
        tree.append(node_hash)

    return build_merkle_tree(tree)


def calculate_merkle_root(leaves):
    tree = build_merkle_tree(leaves)
    return tree


def get_proof(index, leaves):
    proof = []
    leaf_index = index
    tree_size = len(leaves)

    while tree_size > 1:
        sibling_index = leaf_index + 1 if leaf_index % 2 == 0 else leaf_index - 1

        if sibling_index < tree_size:
            proof.append(leaves[sibling_index])

        leaf_index = math.floor(leaf_index / 2)
        tree_size = math.ceil(tree_size / 2)

    return proof


leaves = [hash_leaf(b"Leaf " + str(i).encode()) for i in range(1, 100001)]
merkle_root = calculate_merkle_root(leaves)
print("Merkle Root: ", merkle_root.hex())


# 构建包含关系的证明
index = 66  # 需要构建证明的叶节点索引
proof = get_proof(index, leaves)
print("Proof for leaf", index, ":", [p.hex() for p in proof])


# 构建不包含关系的证明
index = 100002  # 假设不存在的叶节点索引
proof = get_proof(index, leaves)
print("Proof for non-existent leaf", index, ":", [p.hex() for p in proof])
