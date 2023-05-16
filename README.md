![Release](https://img.shields.io/badge/Release-1.2.0-blue)
---
## 介绍
一款部署在多种平台,基于Python-Flask框架,开发的短网址程序.
## 需求
1. 平台: Linux/Vercel/Deta.
2. 语言: Python3.8+.
3. 包: gunicorn,gevent,flask,flask_cors,flask_frozen,pymysql.
4. 数据库: MySql.
## 部署
### 手动
1. 修改config.py.
2. Linux执行gunicorn main:app -c gunicorn.py.
### 自动
Vecel|Deta
---|---
[![Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/H2Oye/H2O-Short-Url)|[![Deta](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy?repo=https://github.com/H2Oye/H2O-Short-Url)
### Vecel
1. 首先点击部署的按钮,等待部署完成.
2. 然后添加环境变量,DATABASE_HOST(数据库地址),DATABASE_PORT(数据库端口),DATABASE_USERNAME(数据库用户名),DATABASE_PASSWORD(数据库密码),DATABASE_NAME(数据库名称),DATABASE_TABLE_PREFIX(数据库表前缀,推荐使用h2o_short_url_),DATABASE_SSL_CA_PATH(CA路径),DATABASE_SSL_KEY_PATH(Key路径),DATABASE_SSL_CERT_PATH(Cert路径),三种证书路径无则空.
![图像1](https://s1.ax1x.com/2023/01/16/pSl2iqK.jpg)
1. 最后重新部署.
![图像2](https://s1.ax1x.com/2023/01/16/pSl2Pr6.jpg)
### Deta
部署时填环境变量.
## 数据库
1. core表修改网站标题,关键词,描述.
2. domain表修改域名,protocol仅能填http/https.
## 问题
1. 问: Vercel/Netlify自带的域名无法访问.  
   答: Vercel/Netlify自带的域名被DNS污染,需要添加自定义域名.