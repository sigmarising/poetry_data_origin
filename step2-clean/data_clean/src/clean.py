import copy
import json
import re
import os


def print_line():
    print("----------------------------------------------------------------------")


def main():
    num_count = {}
    dir_top = "../input/dist/"
    print("开始数据清洗：")
    print_line()

    for dir_dynasty in os.listdir(dir_top):
        num_count[dir_dynasty] = 0
        path_dynasty = os.path.join(dir_top, dir_dynasty)

        for dir_file in os.listdir(path_dynasty):
            path_file = os.path.join(path_dynasty, dir_file)
            f = open(path_file, 'r+', encoding='utf-8')
            text_raw = json.load(f)
            text_target = {
                "dynasty": copy.deepcopy(text_raw["dynasty"]),
                "author": copy.deepcopy(text_raw["author"]),
                "intro": copy.deepcopy(text_raw["intro"]),
                "items": []
            }
            f.close()

            for item in text_raw["items"]:
                num_count[dir_dynasty] += 1
                title = item["title"]
                content = item["content"]

                content = content.split("【注释】")[0]
                content = content.split("【译文】")[0]
                content = content.split("【赏析】")[0]
                r1 = re.compile("（[^）]*）|【[^】]*】|\[[^\]]*\]")
                content = "".join(r1.split(content))
                r2 = re.compile("\{|\[[^\}]*\}")
                content = "".join(r2.split(content))
                r3 = re.compile("\r\n|\n\r|\n|\r")
                content = r3.split(content)

                item_json = {
                    "title": copy.deepcopy(title),
                    "content": copy.deepcopy(content)
                }
                text_target["items"].append(item_json)

            path_target = os.path.join("../output/" + dir_dynasty)
            if not os.path.exists(path_target):
                os.makedirs(path_target)
            f = open(os.path.join(path_target, dir_file), 'w+', encoding='utf-8')
            json.dump(text_target, f, ensure_ascii=False, indent=4)
            f.close()

            print("已处理：", dir_file)
            print("即时统计：", num_count)

    count = 0
    for i in num_count.values():
        count += i
    num_count["summary"] = count
    f = open("../output/summary.json", 'w+', encoding='utf-8')
    json.dump(num_count, f, ensure_ascii=False, indent=4)
    f.close()

    print("诗歌总数：", count)
    print("统计结果已存储至 output/summary.json")


if __name__ == "__main__":
    main()
