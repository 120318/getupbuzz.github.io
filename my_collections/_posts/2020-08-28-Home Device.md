---
layout: post
title: 家里的一些设备
category: Home Device
---

最近这两年一直在折腾家中的网络、媒体、软硬件等，断断续续也搞了好久，最近算是小有所成吧，因而打算在这里写一些文章，一方面算是对自我的一个纪念，另一方面，希望对有相关需求的人能有所启发或帮助。

文章会是一个系列，内容会包括软路由、科学上网、媒体中心、[NAS](https://zh.wikipedia.org/wiki/%E8%99%9B%E6%93%AC%E7%A7%81%E4%BA%BA%E7%B6%B2%E8%B7%AF)、[PT](https://zh.wikipedia.org/wiki/PT%E4%B8%8B%E8%BC%89)等等，软件和硬件都会涵盖，也会叙述一些软硬件选择的心路历程。

本文只是会简要介绍下家中的一些设备，做一个整体的概览，后续会有文章对每个设备与功能单独介绍。

## 拓扑
> *家中设备的拓扑图如下*

![拓扑](/assets/img/home-device.jpg#width-full)

相信有过一些研究的朋友可以看出来，这不是一套昂贵的方案，是一套大部分人都可以考虑的方案，而我个人认为，这是一套比较实用且体验较好的方案，相信可以满足大部分人的很多需求。

值得一说的是，我并没有使用**All in one**的方式来搭建，是因为我始终偏向硬件单一职责，如果所有系统都在同一设备上，通过虚拟化来提供不同功能的话，那么一旦这个硬件出现故障，家中所有的功能都将失效。

一个最简单的例子是，比如**软路由**和**NAS**共享同一硬件，如果因**NAS**导致硬件故障，那么软路由提供的功能同时也会失效，家里的网络就会出现问题。

而将功能和硬件分开，需要尽可能的发挥每个硬件的性能，避免资源的浪费。

## 简介
1. 网络的[ISP](https://zh.wikipedia.org/wiki/%E4%BA%92%E8%81%94%E7%BD%91%E6%9C%8D%E5%8A%A1%E4%BE%9B%E5%BA%94%E5%95%86)是联通，带宽是：下行：`300Mbps`，上行：`30Mbps`
2. 光猫拨号改桥接，使用路由拨号
3. 负责拨号的主路由使用的是[R2S](https://wiki.friendlyarm.com/wiki/index.php/NanoPi_R2S/zh)，这是一个x86架构的[软路由](https://baike.baidu.com/item/%E8%BD%AF%E8%B7%AF%E7%94%B1/4824918)，安装的是[OpenWrt](https://openwrt.org/)系统
4. [斐讯K2P](https://detail.zol.com.cn/wireless_router/index1176025.shtml)路由器在这里的作用其实就是一个无线交换机，家庭中的所有设备都是经过K2P进行上网，使用的是[Padavan](https://github.com/hanwckf/rt-n56u)系统
5. 暴风酷播云2期作为NAS，系统使用[Unraid](https://unraid.net/)，装了两块12T的HDD硬盘，其中一块作为奇偶校验盘，所以共提供12T的存储空间
6. [NUC11猛虎峡谷](https://www.intel.cn/content/www/cn/zh/products/sku/205594/intel-nuc-11-pro-kit-nuc11tnhi5/specifications.html)，版本是i5处理器的厚版，作为家中的计算中心，系统使用了[Ubuntu](https://ubuntu.com/)的21.04版本，运行一些需要24h常驻的应用程序
7. 个人PC，不作过多介绍了，仅仅是一台自组装的台式机罢了
8. 斐讯N1，系统使用[CoreELEC](https://coreelec.org/)，作为视频播放器，连接电视，因为与其他设备不在一个房间，使用了无线网络

## 能力
> *其实想要实现下述这些功能并不麻烦，方案也有很多，但是实际体验和便捷舒适度是我比较看中的，而体验中一个小小的点可能就需要处理很久*

1. 家中全设备科学上网
2. 家中全数据媒体资源存储到NAS中，全设备可通过NAS共享资源访问，同时，外网也可通过[VPN](https://zh.wikipedia.org/wiki/%E8%99%9B%E6%93%AC%E7%A7%81%E4%BA%BA%E7%B6%B2%E8%B7%AF)随时随地访问家中资源
3. 家中全设备共享媒体中心，电脑、手机、电视等设备播放媒体进度可即时同步
4. 因为有PT资源，媒体片源问题得到解决，可观看高质量蓝光、压制视频资源，同时追剧完全可通过[RSS](https://zh.wikipedia.org/zh/RSS)自动化，通过订阅想看的电视剧，即时观看最新剧集
5. 因为存在24h运行、内外网都可访问的Server，你可以随时利用Server的计算资源，去做如：下载资源，跑程序等一切你想做的事。

