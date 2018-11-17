# 诗词曲爬虫 - 开发笔记

written by *Jason Zhang*

## 2018.10.1 开发笔记

> 速览：定义了需要爬取的数据有哪些，如何组织 .json 存储

**Require First**：python3.6 + scrapy + pywin32\
**爬取目标**：国学大师 [诗词曲库](http://www.guoxuedashi.com/shici/)\
**爬取特点**：多级页面，需要进行多级parse处理，不同于常见的下一页链接式爬取

**分析： 任意一个条目(item)，应该有的数据信息（按网页级别进行缩进）**

* **朝代**：秦、汉……
* **作者（出自）**：诗经、班固……
    * **作者（出自）简介**：对作者（出自）的生平描述……
        * **条目名称X**：……
        * **条目正文X**：……

*即item的单位应该是“**朝代_作者**”，以此单位为文件*

可以用 json 组织：**朝代_作者.json**
```json
{
    "dynasty" : "秦",
    "author" : "屈原",
    "intro" : "balabalabala",
    "items" : [
        {
            "title" : "xxxx",
            "content" : "xxxxx"
        },
        {
            "title" : "xxxx",
            "content" : "xxxxx"
        }
    ]
}
```

> 2018.10.6补充：\
> 由于 scrapy 自下而上从 parse 中传递参数变得较为困难，所以可以在最终的 pipeline 处理时再做同作者的诗歌合并，定义 item 时，可以如下定义：
> 
> ```python
> dynasty = scrapy.Field()
> author = scrapy.Field()
> intro = scrapy.Field()
> title = scrapy.Field()
> content = scrapy.Field()
> ```

## 2018.10.5 开发笔记

> 速览：使用 scrapy 在多个 parse 中自上而下逐级传递 item
> 
>  ```python
> # method 1
> import copy
> 
> yield scrapy.Request(
>     url=next_url, 
>     meta={
>         'item': copy.deepcopy(item_before)
>     }, 
>     dont_filter=True, 
>     callback=self.next_parse
> )
> 
> # method 2
> yield scrapy.Request(
>     url=next_url, 
>     meta={
>         'thing1': thing1_before,
>         'thing2': thing2_before
>     }, 
>     dont_filter=True, 
>     callback=self.next_parse
> )
>  ```

### 如何使用 scrapy 进行**多级别的页面传递 item 信息？**

```python
yield scrapy.Request(url=next_url, meta={'item': item}, callback=self.next_parse)
```

Scrapy 用 `scrapy.Request` 发起请求时，可以带上 `meta={'item': item}`，把之前已收集到的信息传递到新请求里。\
在新请求里用 `item = response.meta('item')` 接受过来，item 就可以继续添加新的收集的信息了。

> 参考链接：[Python Scrapy多层爬取收集数据](https://blog.csdn.net/ygc123189/article/details/79160146)

> **2018.10.6 紧急补充**：\
> 注意：meta字段的方法是**浅拷贝**，并非深拷贝，（[可参考官方文档](https://doc.scrapy.org/en/latest/topics/request-response.html#request-objects)），所以如果 item 有多个字段时，要么在meta中多字段表示，要么使用深拷贝方法。\
> 使用方法可见速览。

###  是否需要进行 **url去重操作？**

如果二级页面的 url 是根据某内容来定义 *url路径* 的，因此会存在很多重复的 二级url，需要不去重操作。

> 去重机制：`scrapy.Request()` 的参数 `dont_filter` 默认是 `False`（去重）。\
> 每 yield 一个 `scrapy.Request()`，就将 url参数 与调度器内已有的 url 进行比较，如果存在相同 url 则默认不入队列，如果没有相同的 url 则入队列，\
> 如果想要实现不去重效果，需要将 `dont_filter` 改为 `True`
> 
> 来自参考链接：[spider爬取多级url](https://blog.csdn.net/loner_fang/article/details/81031075)

## 2018.10.6 开发笔记

### 工程配置

* 配置工程，不遵守 `robot.txt`，避免不必要的麻烦
* 配置工程，0.25s 下载时延
* 网站使用 scrapy 默认 useragent 即可进行抓取
* 启用pipeline
* 自定义useragent
* 启用日志warning级别

### scrapy selector 的 extract 与 extract_first 方法

* `extract` 以列表形式（记此列表为`a`）返回选择器中的 data 字段，\
  `extract_first` 则返回上述列表`a`中的第一个元素（多为字符串）
* 通常 `extract` 得到的列表中，只有一个元素，所以往往用 `extract_first` 即可。\
  但若 `extract` 得到的列表中有多个元素，则需要使用 `''.join(a)` 得到具体的字符串信息。
* `' xxx '.strip()` 可以用于去掉头尾空白字符

### 工作方法

parse拆分各个朝代，parse_author拆分各个作者，parse_poetry拆分各个具体的诗。

### 存储 json 文件

由于我们定义的 item 与我们的 目标json文件 有一定的差距，所以我们不可以使用 scrapy 的 Feed export，而需要在 pipeline 中进行编写自定义的方法。

> [参考链接](https://doc.scrapy.org/en/latest/topics/item-pipeline.html#write-items-to-a-json-file)

### 编写 pipeline 注意事项

* 首先需要在设置中启动pipeline，才可以有效果
* mkdir创建单级目录，makedirs创建多级目录
* 需要首先`dict(item)`
* 打开文件时
    * w 只可以写文件
    * w+ 可读可写，打开后立即清空
    * r 只可以读文件
    * r+ 可读可写
    * encoding 保存中文必选
* 写json时，注意使用`"`而非`'`
* `json.dump(text, f, ensure_ascii=False, indent=4)`可保存中文，并格式化json

### 启用 scrapy 日志功能

详细见参考链接

> [Scrapy logging settings](https://doc.scrapy.org/en/latest/topics/logging.html#logging-settings)

## 2018.10.7 开发笔记

设置 `DOWNLOAD_DELAY = 0.25` 时，爬取速度过慢，4小时仍未爬取完毕\
因此设置为 `DOWNLOAD_DELAY = 0.1`
