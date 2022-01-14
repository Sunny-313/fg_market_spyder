
<!--
 * @Description: 
 * @version: 
 * @Author: Sunny
 * @Date: 2022-01-14 11:01:22
 * @LastEditors: Sunny
 * @LastEditTime: 2022-01-14 14:27:26
-->
<!-- TOC -->

- [飞瓜数据中关于市场大盘的数据爬取](#飞瓜数据中关于市场大盘的数据爬取)
    - [获知参数变化的值](#获知参数变化的值)
    - [copy curl 验证是否能够下载文件](#copy-curl-验证是否能够下载文件)
    - [在Network中寻找 .xhr文件（这是个人经验，需要长时间积累）](#在network中寻找-xhr文件这是个人经验需要长时间积累)
    - [将找到的.xlr文件点开搜索需要的代码段](#将找到的xlr文件点开搜索需要的代码段)
    - [python读入json处理，将其解析转成Dataframe](#python读入json处理将其解析转成dataframe)
    - [本次实操需要注意的点](#本次实操需要注意的点)

<!-- /TOC -->

# 飞瓜数据中关于市场大盘的数据爬取

##  获知参数变化的值
- 1.![1](pic/16b7f4f80f0eb5940eebfa2caf4bbe08.png)
- 2.查看变量参数的变化，在界面操作点击不同的变量参数位置，洞悉不同参数变量的改变 
- 3.![2](pic/2b863d2d14a6e4efefe4d12f514233ae.png)
  ![3](pic/dd2a8d92ccdb1c17df0957fb49063e89.png)
  ![4](pic/9b560e807fbef1d024ceeb78dc13b209.png)
## copy curl 验证是否能够下载文件
- ![5](pic/3f42e92a11144c038a23a08b164b04f3)
<font color = "	#EEB4B4" size = '4'> copy as curl(bash)命令测试</font>

## 在Network中寻找 .xhr文件（这是个人经验，需要长时间积累）
- ![6](pic/303565c1cccf02de0bb650864cf33712.png)
## 将找到的.xlr文件点开搜索需要的代码段
- ![7](pic/96e33633168eb549b01c8be36e1ceab4.png)
- 快速获取我们想要的json文件可以直接copy response产品的类目到notepad++然后删除我们不需要的部分
![8](pic/d371ccce4c013b8d89fd199d9341d616.png) 
##  python读入json处理，将其解析转成Dataframe
- 这里直接使用pd.DataFrame()来操作



## 本次实操需要注意的点
- 延迟处理
>延迟处理最好保证时间的随机性
  时间保持在30s以上
- 判断文件是否存在，如果存在则不下载，直接跳过
> 对于下载过的文件不进行重复下载处理
> 这里使用os.path.isfile()方法
- 超时处理
> 对于爬取的过程中会出现timeout的情况，要对这部分数据进行提前预判
> 主要使用try ……exption……