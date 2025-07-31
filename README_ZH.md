

<h1 align="center">superduper智数融合平台</h1>
<p align="center">
  <a href="README.md"><strong>English</strong></a> | <strong>简体中文</strong>
</p>





## 目录

- [仓库简介](#项目介绍)
- [前置条件](#前置条件)
- [镜像说明](#镜像说明)
- [获取帮助](#获取帮助)
- [如何贡献](#如何贡献)

## 项目介绍

[superduper](https://github.com/superduper-io/superduper) 是一款面向开发者和企业的AI应用开发与数据库集成平台，能够简化AI模型与Qdrant、MySQL等多种数据库交互。旨在降低AI应用落地门槛，提供模块化、可扩展的工具链，帮助快速实现RAG检索增强生成、智能问答等场景。本商品基于鲲鹏服务器的Huawei Cloud EulerOS 2.0 64bit系统，提供开箱即用的superduper。

## 核心特性

- **AI 模型与数据库无缝集成：** 支持将大语言模型、嵌入模型、分类器等 AI 模型直接“插入”现有数据库（如 MongoDB、SQLite），实现数据的自动扩展与智能增强
- **动态向量存储与检索：** 在数据写入时自动调用模型生成嵌入向量并存储，开箱支持语义搜索、相似性匹配与向量化查询，无需额外构建同步管道

本项目提供的开源镜像商品 [superduper智数融合平台](https://marketplace.huaweicloud.com/hidden/contents/3105d1ab-eed7-48bc-9961-5d53369c6012#productid=OFFI1146359918988120064) 已预先安装0.7.0版本的superduper及其相关运行环境，并提供部署模板。快来参照使用指南，轻松开启“开箱即用”的高效体验吧。

> **系统要求如下：**
>
> - CPU: 2vCPUs 或更高
> - RAM: 4GB 或更大
> - Disk: 至少 40GB

## 前置条件

[注册华为账号并开通华为云](https://support.huaweicloud.com/usermanual-account/account_id_001.html)

## 镜像说明

| 镜像规格                                                     | 特性说明                                                 | 备注 |
| ------------------------------------------------------------ | -------------------------------------------------------- | ---- |
| [superduper-0.7.0-kunpeng](https://github.com/HuaweiCloudDeveloper/superduper-image/tree/superduper-0.7.0-kunpeng) | 基于鲲鹏服务器 + Huawei Cloud EulerOS 2.0 64bit 安装部署 |      |

## 获取帮助

- 更多问题可通过 [issue](https://github.com/HuaweiCloudDeveloper/superduper-image/issues) 或 华为云云商店指定商品的服务支持 与我们取得联系
- 其他开源镜像可看 [open-source-image-repos](https://github.com/HuaweiCloudDeveloper/open-source-image-repos)

## 如何贡献

- Fork 此存储库并提交合并请求
- 基于您的开源镜像信息同步更新 README.md
