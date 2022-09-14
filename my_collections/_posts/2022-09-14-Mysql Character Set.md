---
layout: post
title: MySQL字符集
category: Database
---
整体来说，`MySQL`内部的字符集还是略微复杂的，而我们平时使用过程中也经常会遇到一些字符串乱码问题，没错，我就是遇到了这个问题，本想简单解决，却发现情况比预期的略微复杂。

这里希望本文可以让你真正找到你所遇到的问题的原因与解决方案。
## 字符集
首先需要介绍一下**字符集**的概念，我们知道计算机是只能存储二级制数据的，而字符集的作用就是帮助你将平时遇到的各种文字映射成二进制数据。将文字转换成二进制称为字符编码，将二进制转换成文字称为字符解码。

这里先介绍3种最最常见的字符集，方便理解概念。
### ASCII
`ASCII`全称是American Standard Code for Information Interchange，是基于拉丁字母的一套电脑编码系统。但其只包含128个字符，包括基本英文字符，阿拉伯数字以及英文标点符号，所以其主要用于显示现代英语，但对于其他语言乃至Emoji表情符号等，`ASCII`就无能为力了。

编码举例：
```
'L' ->  01001100（十六进制：0x4C）
```
### Latin1
也称作`ISO 8859-1`，`Latin1`是**单字节**编码，向下兼容`ASCII`，共收录了256个字符，在`ASICC`的基础上又扩充了128个西欧常用字符，可以说是对`ASCII`的一个补充。 256个字符就厉害了，一个字节由256个字符组成，这样它可以对**任意单字节**进行编码。

编码举例：
```
'L' ->  01001100（十六进制：0x4C）
'à' ->  11100000（十六进制：0xE0） 
```
### UTF-8
`UTF-8`（8-bit Unicode Transformation Format）是一种针对Unicode的可变长度字元编码，可以说`UTF-8`是`Unicode`编码的一种实现，它整理、编码了世界上大部分的文字系统，使得电脑可以用更为简单的方式来呈现和处理文字，也就是说他可以很好的支持中文以及其他各国语言。自2009年以来，`UTF-8`一直是万维网的最主要的编码形式，它同样也向下兼容`ASCII`，也正是由于它的普及，我们平时经常见到，甚至正在使用的大都是这种字符集。

编码举例：
```
'L' ->  01001100（十六进制：0x4C）
'啊' ->  111001011001010110001010（十六进制：0xE5958A）
```
## MySQL中的字符集
为了便于解释，先安装一个`MySQL Server(5.7)` 和 `MySQL CLI(MyCLI)`。

首先查看一下当前MySQL中的一些字符集相关的变量
```sql
mysql root@localhost:(none)> SHOW VARIABLES LIKE 'character%';
+--------------------------+----------------------------+
| Variable_name            | Value                      |
|--------------------------+----------------------------|
| character_set_client     | utf8                       |
| character_set_connection | utf8                       |
| character_set_database   | latin1                     |
| character_set_filesystem | binary                     |
| character_set_results    | utf8                       |
| character_set_server     | latin1                     |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+
8 rows in set
Time: 0.009s
```

> `MySQl 5.7`默认使用的字符集 就是`Latin1`。

* **`character_set_client`**： MySQL Server解码客户端传来的Query字符串所使用的字符集，在上面例子中，服务端收到`SHOW VARIABLES LIKE 'character%'`这条命令的字节流，会认为其是UTF-8编码。
* **`character_set_connection`**：服务端收到请求执行Query时会将`character_set_client`的字符集转换为`character_set_connection`的字符集，当前的变量设置中二者字符集是一致的，不需要转换。
* **`character_set_database`**： 数据库的默认字符集。
* **`character_set_filesystem`**：会将Query中的文件名转化成此字符集，比如在`LOAD DATA` Query中，对于其中的文件名，会认为其是`character_set_client`，并将其转换成`character_set_filesystem`， 默认值就是binary，意思就是不做任何转换的，只关注二进制流。
* **`character_set_results`**：MySQL Server将查询结果返回给客户端时所使用的字符集。
* **`character_set_server`**：MySQL Server的默认字符集
* **`character_set_system`**：数据库存储系统元数据使用的字符集，默认是`utf8`。
* **`character_sets_dir`**：字符集文件所在的目录

我们在建表，建库的时候，可以在数据库、表、字段的后面加上字符集相关参数。
这里我们创建一个名为`testdb`的数据库和一张名为`test`的表：
```sql
MySQL root@localhost:testdb> CREATE DATABASE `testdb` DEFAULT CHARACTER SET latin1;
MySQL root@localhost:testdb> USE `testdb`;
MySQL root@localhost:testdb> CREATE TABLE `test` (
  `latin1_name` varchar(255) CHARACTER SET latin1,
  `utf8mb4_name` varchar(225) CHARACTER SET utf8mb4,
  `default_name` varchar(225)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8
```
对于某个字段来说，它所使用的字符集的优先级为：**字段字符集->表字符集->数据库字符集->服务端字符集**。

根据此规则以及上面的MySQl字符集变量，对于`testdb`中未显示指定字符集的表或者字段，将默认使用`latin1`字符集, `test`表使用`utf8`字符集，表中各字段的字符集如下：
| 字段名 | 字符集 |
| ---- | ---- |
| latin_name | latin1 |
| utf8mb4_name | utf8mb4 |
| default_name | utf8 |
### utf8与utf8mb4
这里出现了一个叫`utf8mb4`的字符集，实际上这才是MySQL中真正的`utf8`字符集，而MySQL中的`utf8`实际上是一个阉割版的`utf8`字符集，它是`utf8mb3`，他每个字符最长只有3字节，是不完全的，这是MySQL的一个历史问题。
### 查询中字符集的转换过程
这里重点介绍下在Query请求中，`character_set_connection`、`character_set_client`以及`character_set_results`，这三个变量与请求的字符集的转换关系，整个过程如下图：
> 图片来自[此文]((https://relph1119.github.io/mysql-learning-notes/#/mysql/03-%E4%B9%B1%E7%A0%81%E7%9A%84%E5%89%8D%E4%B8%96%E4%BB%8A%E7%94%9F-%E5%AD%97%E7%AC%A6%E9%9B%86%E5%92%8C%E6%AF%94%E8%BE%83%E8%A7%84%E5%88%99?id=%e5%ad%97%e7%ac%a6%e9%9b%86%e5%92%8c%e6%af%94%e8%be%83%e8%a7%84%e5%88%99%e7%ae%80%e4%bb%8b))

![151539928.jpeg](/assets/img/mysql-charset-convert-procedure.png#width-full)
#### 存储数据使用`Latin1`字符集会有什么问题？
首先我们要明确，如果把`utf8`当做字节流处理，`latin1`是可以对其进行编码的，因为`latin1`是单字节编码的，但是反之则不行。所以无论客户端和数据存储使用什么编码，只要将`character_set_connection`、`character_set_client`以及`character_set_results`都设置成`latin1`，那么一切都会是正确的，举例来说：
```sql
MySQL root@localhost:(none)> set names latin1;

MySQL root@localhost:(none)> SHOW VARIABLES LIKE 'character%';
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | latin1                     |
| character_set_connection | latin1                     |
| character_set_database   | latin1                     |
| character_set_filesystem | binary                     |
| character_set_results    | latin1                     |
| character_set_server     | latin1                     |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+

MySQL root@localhost:testdb> SHOW FULL COLUMNS FROM test;
| Field        | Type         | Collation          | Null | Key | Default | Extra | Privileges                      | Comment |
+--------------+--------------+--------------------+------+-----+---------+-------+---------------------------------+---------+
| latin1_name  | varchar(255) | latin1_swedish_ci  | YES  |     | <null>  |       | select,insert,update,references |         |
| utf8mb4_name | varchar(225) | utf8mb4_general_ci | YES  |     | <null>  |       | select,insert,update,references |         |
| default_name | varchar(225) | utf8_general_ci    | YES  |     | <null>  |       | select,insert,update,references |         |
+--------------+--------------+--------------------+------+-----+---------+-------+---------------------------------+---------+

MySQL root@localhost:testdb> INSERT INTO `test` (`latin1_name`, `default_name`) VALUES ('红', '红');

MySQL root@localhost:testdb> select `latin1_name`, `default_name` from test WHERE `latin1_name`='红';
+-------------+--------------+
| latin1_name | default_name |
+-------------+--------------+
| 红          | 红           |
+-------------+--------------+
```
我们可以看出虽然`latin1_name`和`default_name`分是`latin1`和`utf8`编码，但，我们对于中文`红`的都能够正确读取和显示。

值得一提的是，对于`default_name`，因为客户端和存储数据都使用的是`utf8`，但是`client, connection, results`使用的却是`latin1`，这会导致字符经过了两次`utf8`编码（Double Encoding）

1. Client将其编码成`utf8`传输到MySQL Server
2. 而MySQL Server却认为这是`latin1`
3. 由于存储数据使用`utf8`字符集，这时MySQL Server把其当做`Latin1`字节流，再次对齐进行`utf8`编码。

上面说的二次编码问题，不会对读取和显示造成什么影响，但是如果需要对该字段进行排序，可能会导致，排序结果不符合你的预期。
### 比较规则
说到排序与比较，这里也浅提一嘴`比较规则`。
对于不同的字符集会有不同的比较规则，当你设置好字符集时，MySQL会自动帮你设置好该字符集的默认比较规则，一般情况我们不需要去修改（`utf8`默认为`utf8_general_ci`）。除了一些特殊情况：比如你需要区分大小写，轻重音等等。
## 总结
说了这么多，其实你只要无脑的将相关的编码都设置成`utf8mb4`，在现代应用中，几乎是不会遇到乱码问题的。

最后力荐一篇Mysql字符集相关Blog：[sql.rjweb.org](sql.rjweb.org/doc.php/charcoll)，它解决了我在MySQL字符集上的的很多困惑。
## 参考
* [《MySQL 是怎样运行的：从根儿上理解 MySQL》](https://relph1119.github.io/mysql-learning-notes/#/mysql/03-%E4%B9%B1%E7%A0%81%E7%9A%84%E5%89%8D%E4%B8%96%E4%BB%8A%E7%94%9F-%E5%AD%97%E7%AC%A6%E9%9B%86%E5%92%8C%E6%AF%94%E8%BE%83%E8%A7%84%E5%88%99?id=%e5%ad%97%e7%ac%a6%e9%9b%86%e5%92%8c%e6%af%94%e8%be%83%e8%a7%84%e5%88%99%e7%ae%80%e4%bb%8b)
* 维基百科