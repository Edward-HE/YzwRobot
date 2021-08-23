# 研招网数据爬虫项目

本项目 fork 自 [yzw](https://github.com/Hthing/yzw) ，是原项目功能的修改版。主要功能为 https://yz.chsi.com.cn/zsml/queryAction.do 页面的数据爬取。

## Features

- 所在省市、门类类别、学科类别可以选为空，实现对某一省市、某一学科所有学校的批量爬取
- 去除数据库存储和 excel 存储，改为 csv 格式存储
    - MySQL 写入可能存在写锁问题，数据丢失严重，待日后研究后考虑是否加入
    - excel 格式不适合大量数据写入，xlwt 只能写入 .xls 格式，且一次只能写入 65535 条数据
    - csv 对文件逐行写入性能更优，且导入到 DB 以及 excel 中更方便

## TODO

-   [ ] ~~MySQL 写入可能存在写锁问题，数据不能完全写入，有部分丢失~~

## Usage

## 1. 配置环境

``` bash
pip install -r requirements.txt
```

## 2. 修改配置

配置文件目录 `YzwRobot\yzw\settings.py`，可以修改爬取范围，包括省份、门类代码(01)、一级学科代码(0101)，如果爬取所有数据可以不修改。

## 3. 运行程序

主程序文件为 `YzwRobot\main.py`

运行结果示例如下
![img.png](img/img_5.png)