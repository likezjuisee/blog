# 服务端性能测试方案对比结果

服务端的性能测试是测试领域的主要需求，国外公司出品的测试工具，例如Jmeter和Loadrunner等，依靠出色的产品设计和实现方案，现在依然是众多公司做性能测试的主要方案。

近年，随着技术发展，一些替代方案出现了。其中以python和go的增长速度尤为突出，python得益于其快速简单的开发周期，go得益于其高性能和并发编程的简易性。

## 常用的方案

- Jmeter [https://github.com/apache/jmeter](https://github.com/apache/jmeter "Jmeter")
- LoadRunner [http://www8.hp.com/us/en/software-solutions/loadrunner-load-testing/](http://www8.hp.com/us/en/software-solutions/loadrunner-load-testing/)
- Locust（python2.7） [https://github.com/locustio/locust](https://github.com/locustio/locust)
- asyncio （python3.5）[https://github.com/python/asyncio](https://github.com/python/asyncio)
- go [https://github.com/golang/go](https://github.com/golang/go)
 
Jmeter不做过多介绍

LoadRunner由于是收费版本，没有列为对比内容之一

Locust是近年出现的基于python2.7 greenlet gevent协程库开发的单线程多协程的压力测试框架

asyncio是python3.5语言内置的协程库，相对2.7进行了优化，并且提供了相关的http请求的库 [https://github.com/KeepSafe/aiohttp](https://github.com/KeepSafe/aiohttp)

go语言内置对并发编程提供了强大的支持，依靠其类C的性能，成为服务端开发高性能组件的主要语言。http请求也开源了一个新的库[https://github.com/valyala/fasthttp](https://github.com/valyala/fasthttp)

## 测试目标
从性能测试工程师的角度出发，我们其他用更少的硬件资源实现更大的并发压力。期望通过对比，选取其中最优的方案（资源消耗低，压力大），作为性能测试的实现方案。

## 测试环境

- 服务端 centos 4核16G
- 服务端软件 openrestry 2 worker （类似nginx） 
- 客户端 ubuntu 2核2G
- GET请求静态页面

## 测试方案
对比并发用户数是10,50,100,500,1000时，客户端CPU、内存消耗，服务端被测软件cpu负载，以及关键数据TPS。

HTTP GET请求nginx静态页面，磁盘的IO负载较低，本次不作为对比项。

## 对比结果

![](http://i.imgur.com/i2nd9G8.png)
![](http://i.imgur.com/kgN2SRy.png)
![](http://i.imgur.com/CjvZ2eq.png)
![](http://i.imgur.com/rG77Qo1.png)

## 结论
- python3.5的协程实现相对2.7，在高并发1000个用户，每个用户一个协程，提升了100%，可以基于aiohttp的库开发性能测试框架。
- Jmeter的java线程实现优于python，解释型与编译型语言还存在着一定差距。但是在扩展性上，python的框架由于是自主开发，对于多种协议的支持门槛很低。Jmeter的最新版本还不支持websocket协议。
- go的结果最为优秀，TPS是Jmeter的两倍以上，尤其是在高并发场景中，效果明显。

## 愿景
基于go的性能测试平台正在开发中，敬请期待。