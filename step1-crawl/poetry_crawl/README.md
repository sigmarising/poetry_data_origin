# 古诗词爬虫

本项目是针对于： [国学大师-诗词曲库](http://www.guoxuedashi.com/shici/) 的爬虫

> [诗词曲库-备用地址](http://gx.guoxuemi.com/)

## 项目所需

* Python 3.6
* Scrapy 1.5.1
* pywin32 224 (windows平台运行所需)

## 如何运行项目

1. 进入到项目的根目录，删除 `poetry_crawl.log `以及 `dist/`，若文件不存在则直接进行第二项
2. 在根目录启动命令行，输入：

```terminal
scrapy crawl poetry_spider
```

## 输出

 `dist/`目录下的数据，以及根目录下的日志文件。

> 爬取时间大约6小时，为了方便使用，`dist.zip` 为完整运行爬虫后的输出数据打包。如有需要直接下载即可。

## 其他

关于项目的开发思路以及开发笔记，\
可参见[`Notes/DevNotes.md`（点击即可访问）](./Notes/DevNotes.md)