# 南京室外温度检测服务

## 介绍
本节点为海萤物联网提供南京室外温度检测服务。具体位置是南京市江北新区。

本节点是一个设备，esp32板子外接ds18b20传感器。这个传感器是防水的，放在室外，所以能够检测室外温度。

![输入图片说明](https://images.gitee.com/uploads/images/2021/0408/075120_3357e2fb_5148492.png "屏幕截图.png")

## 本节点地址
```text
0x2141000000010001
```

## 服务
服务号|服务
---|---
1|读取南京室外温度

### 读取南京室外温度
- CON请求：空

- ACK应答：

字段|字节数
带符号温度值.分度0.1摄氏度|2

应答的是字节流，大端格式。温度分度是0.1摄氏度，所以假设两个字节是0x00 0xe8，则对应的温度是0x00e8=232=23.2摄氏度。

温度值是带符号的数，所以如果温度大于0x8000，则温度为负数。C语言直接使用int16_t强制转换即可，其他语言可以使用0x10000-温度值算出温度值。
比如温度值0xff18，使用0x10000-0xff18=232，所以温度是-23.2摄氏度。
