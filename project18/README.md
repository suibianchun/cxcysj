**Project18: send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself**

进入blockcypher.com网站，可以看到 api.blockcypher.com作为API接口，我使用api.blockcypher.com/v1/btc/main

**网站截屏：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/5529a621-b872-4417-bdd7-585422a79b39)

**运行结果：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/769ce5a8-88dc-4347-b66f-81963ffd04bf)

**部分参数解释：**

"name": "BTC.main"：代表比特币（Bitcoin）的主网，是比特币网络的主要区块链网络。

"height": 798052：表示当前区块的高度，即区块链中该区块所在位置的索引值。

"hash": "00000000000000000005533301cdaa284dafb79b2e30762f1bd30035017a37bb"：表示当前区块的哈希值，是一个64位的十六进制字符串，用于唯一标识该区块。

"time": "2023-07-10T03:23:08.722760991Z"：表示当前区块的时间戳，即该区块被挖出的时间。

"previous_hash": "00000000000000000000b3e54637f010fc50fce9240fa3a8b6f61247eccc1589"：表示前一个区块的哈希值，即当前区块的上一个区块。

"last_fork_height": 795426：表示最近的分叉（fork）发生时的区块高度，即最近一次出现两个或多个不兼容的区块链版本的高度。

"last_fork_hash": "000000000000000000045d66a7991b54de7e11776eed27e34df24a59b7de370e"：表示最近的分叉（fork）发生时的区块哈希值，是一个64位的十六进制字符串，用于标识最近一次分叉时的区块。

