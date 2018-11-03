# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json

class PoetryCrawlPipeline(object):
    def open_spider(self, spider):
        print("crawl start......")

    def close_spider(self, spider):
        print("crawl complete!")

    def process_item(self, item, spider):
        # convert to dict first
        i = dict(item)

        # dist/ is the output dir
        if not os.path.exists('./dist'):
            os.mkdir('./dist')

        dir_dynasty = './dist/' + i['dynasty']
        dir_file = './dist/' + i['dynasty'] + '/' + i['dynasty'] + '_' + i['author'] + '.json'

        if not os.path.exists(dir_dynasty):
            os.makedirs(dir_dynasty)

        if not os.path.exists(dir_file):
            f = open(dir_file, 'w+', encoding='utf-8')
            text = {
                "dynasty": i["dynasty"],
                "author": i["author"],
                "intro": i["intro"],
                "items": [
                    {
                        "title": i["title"],
                        "content": i["content"]
                    }
                ]
            }
            json.dump(text, f, ensure_ascii=False, indent=4)
            f.close()

        else:
            f = open(dir_file, 'r+', encoding='utf-8')
            text = json.load(f)
            text["items"].append(
                {
                    "title": i["title"],
                    "content": i["content"]
                }
            )
            f.close()

            f = open(dir_file, 'w+', encoding='utf-8')
            json.dump(text, f, ensure_ascii=False, indent=4)
            f.close()

        # stdout info
        print("已处理：" + i['dynasty'] + "_" + i['author'] + "_" + i["title"])

        return item
