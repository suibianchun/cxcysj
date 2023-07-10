import requests

url="https://api.blockcypher.com/v1/btc/main"


#get操作访问指定的url
response=requests.get(url)
response.encoding="utf-8"
message=response.text

#将数据写入bitcoin.txt中
with open("bitcoin.txt","wb") as f:
     f.write(message.encode("utf-8"))
