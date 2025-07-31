# superduper部署指南



## ‌一、环境准备



### 更新系统



#### EulerOS2.0



```
yum -y update  
yum -y upgrade
```



#### Ubuntu 24.04



```
apt-get -y update
export DEBIAN_FRONTEND=noninteractive
apt-get -y -o Dpkg::Options::="--force-confold" dist-upgrade
```



## ‌二、安装docker



#### EulerOS2.0



参考：[安装Docker](https://support.huaweicloud.com/bestpractice-hce/hce_bp_0002.html)

#### Ubuntu 24.04



参考：[安装Docker](https://www.runoob.com/docker/ubuntu-docker-install.html)

## **三、安装conda**



```
mkdir -p ~/miniconda3

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O ~/miniconda3/miniconda.sh

bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3

rm -f ~/miniconda3/miniconda.sh

source ~/miniconda3/bin/activate

conda init --all
```



创建虚拟环境

```
conda create -n superduper python=3.10
```

## **四、源码下载**

### **1.下载源码**

```
git clone https://github.com/superduper-io/superduper.git

git clone https://github.com/qdrant/qdrant.git

pip install qdrant-client -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install modelscope -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install superduper-framework==0.7.0 -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install superduper-qdrant==0.7.0 -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install sentence-transformers -i https://pypi.tuna.tsinghua.edu.cn/simple 
```



### **2.下载模型**

```
modelscope download --model sentence-transformers/all-MiniLM-L6-v2 --local_dir /home/model/all-MiniLM-L6-v2

mkdir -p /session/secrets
```



## **五、启动项目**

### **1.修改代码**

[app.py](../scripts/app.py)




### **2.运行实现**

首先启动qdrant服务：

```
docker run -p 6333:6333 qdrant/qdrant
```

然后就能打开网页 https:ip:6333/dashboard

![img](images/img_1.png)

运行代码为：

```
python app.py
```

![img](images/img_2.png)

主要实现是将一组数据通过模型编码为向量，并添加到qdrant数据库中，然后使用进行查询，输出结果。

Qdrant用来存储向量数据，高效邻近搜索。

SuperDuperDB 是一个 AI-native 数据抽象层，用于简化 ML 模型与数据库之间的交互。
