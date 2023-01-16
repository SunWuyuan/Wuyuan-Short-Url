![Release](https://img.shields.io/badge/Release-1.1.0-blue)
---
## 介绍
一款部署在多种平台,基于Python-Flask框架,开发的短网址程序.
## 演示站
[https://url.h2oa.icu](https://url.h2oa.icu)
## 需求
1. 平台: Windows/Linux/Vercel/Deta/Netlify.
2. 语言: Python.
3. 包: gunicorn,gevent,flask,flask_cors,pymysql.
4. 数据库: MySql.
## 部署
### 手动
如果需要在Windows/Linux上部署,Windows运行main.py,Linux执行gunicorn main:app -c gunicorn.py.
### 自动
Vecel|Deta|Netlify
---|---|---
[![Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/H2Oa/H2O_Short_Url)|[![Deta](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy?repo=https://github.com/H2Oa/H2O_Short_Url)|[![Netlify](https://www.netlify.com/img/deploy/button.svg)](https://dashboard.4everland.org/hosting/new?type=clone-flow&s=https://github.com/H2Oa/H2O_Short_Url)
## 安装
1. 如果是手动部署,先修改config.py,然后运行/执行.
2. 如果是自动部署,先Fork,然后修改config.py,最后点击部署的按钮.
## 配置
1. core表修改网站标题,关键词,描述.
2. domain表修改域名,protocol仅能填http/https.
## 问题
1. 问: Vercel/Netlify自带的域名无法访问.  
   答: Vercel/Netlify自带的域名被DNS污染,需要添加自定义域名.
## 版本
### 1.0
氧化氢短网址程序问世.
### 1.1
1. 增加多种平台的部署.
2. 优化显示.
3. 修改文档.