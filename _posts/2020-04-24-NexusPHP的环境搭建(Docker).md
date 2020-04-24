---
layout: post
title: NexusPHP的环境搭建(Docker)
category: Other
---
# 前言
1. [NexusPHP](https://github.com/ZJUT/NexusPHP)不作过多介绍
2. 此类教程网上已有很多，其实无非就是[LNMP](https://zh.wikipedia.org/zh-hans/LAMP)的环境搭建，所以相关开发人员应该无须阅读本文
3. 建议开发/测试环境采取本文所述方法，对于生产环境，本文不对其参数进行保证

# 方式
> 最简单的方式应该就是使用已经Build好的Docker镜像，免去LNMP环境的安装，拉取即用

1. 安装Docker

    你需要安装并能够使用Docker，安装方式详见[官网](https://docs.docker.com/get-docker/)即可。

2. 拉取并启动镜像

    地址：[dockerhub](https://hub.docker.com/repository/docker/dearjoey/nexusphp), [github](https://github.com/dearjoey/NexusPHP-Docker)

    拉取与启动方式详见上述链接中的README介绍。

3. 配置DB

   查看NexusPHP源码配置，配置文件在`config/allconfig.php`,主要查看部分如下：
   ```php
   $BASIC=array(
	'SITENAME' => 'expample.com',
	'BASEURL' => 'localhost',
	'announce_url' => 'localhost/announce.php',
	'mysql_host' => 'localhost',
	'mysql_user' => 'nexusphp',
	'mysql_pass' => '123456',
	'mysql_db' => 'nexusphp',
    )
   ```
   上面的Docker镜像内置安装了`phpmyadmin`，所以可以通过`phpmyadmin`初始化NexusPHP数据库表，直接访问[http://localhost/pma/index.php](http://localhost/pma/index.php)（当然，也可直接通过命令行直接操作）

    1. 新建Database，名字对应上面配置中`mysql_db`字段的值
    2. 新建用户，配置用户名和密码分别对应为上面配置中`mysql_user`和`mysql_pass`字段中的值
    3. 将NexusPHP源码中的`_db/dbstructure.sql`导入到上面所建的Database中

至此，NexusPHP环境搭建完毕，你应该已经可以访问[http://localhost/index.php](http://localhost/index.php)。

**Now, enjoy!**

# FAQ
