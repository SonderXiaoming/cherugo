# 切噜一下

# HoshinoBot原生插件魔改

## 简介

适用于 [HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot) 的娱乐性增强， 修改 `modules/priconne/cherugo.py` 文件

### ★ 如果你喜欢的话，请给仓库点一个star支持一下23333 ★

## 本项目地址：

https://github.com/SonderXiaoming/cherugo

## 魔改内容

切噜一下之后会发送一段伪装切噜语音

## 原理

读取切噜文件夹下的语音文件

将人话翻译为切噜语，然后根据其字数长度随机拼接语音并发送（语音文件名即是语音文件说的话，字数相同也是随机选择）

即：只是保证了字数一样

所以是伪切噜语音

(要不丢[知更鸟](https://github.com/babysor/MockingBird)训练一下，水平不够，欢迎pr，只要训练好的模型就行，对接我可以，或者其他训练)

## 部署教程：

0. 本插件运用了[HoshinoBot增强-语音调用支持](https://github.com/Soung2279/advance_R)，偷了个小懒，要用本插件先装这个

此插件调用了非常用库，如果没装，请依次使用如下指示安装依赖（其他你们应该装了，大概）

打开cherugo文件，点击上方菜单“文件”，选择打开powershell，输入 pip install pydub

1. 下载或git clone本插件：

   在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目

   ```
   git clone https://github.com/SonderXiaoming/cherugo
   ```

2. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'cherugo'

3. 删除``modules/priconne/cherugo.py`` 

## 已知问题（不会做或懒得做，最好有大佬pr）

1. 语音怪怪的，我觉得是素材问题，我素材是直接从b站下的切噜语初级和中级讲座视频，然后用pr一剪，大佬pr个素材
2. 其实最好训练个模型，我目前只知道[知更鸟](https://github.com/babysor/MockingBird)比较好
3. 做个映射，保障同样的话用的是相同的语音拼接

## 鸣谢

[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)
