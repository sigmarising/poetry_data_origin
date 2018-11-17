"""
Author: Zihe Liu
Date: 2018.11.14
---
Modifyer: Yun Zhang
Date: 2018.11.17
"""

import json
import os
import re
import pymysql


INPUT_DIR = "../input/dist/"
MYSQL_URL = "localhost"
MYSQL_USER = "root"
MYSQL_PWD = "zhangyun"
MYSQL_DB = "gelai"


def main():
    dir_top = INPUT_DIR
    db = pymysql.connect(MYSQL_URL, MYSQL_USER, MYSQL_PWD, MYSQL_DB, charset='utf8')
    cursor = db.cursor()  # 创建并返回游标
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s " % data)  # 结果表明已经连接成功
    cursor.execute("DROP TABLE IF EXISTS poetry")  # 诗歌 sheet
    cursor.execute("DROP TABLE IF EXISTS poet")  # 诗人 sheet

    sql1 = """
    create table poetry (
        id int(11) not null primary key auto_increment,
        author_id int(11) default 0,
        title varchar(255) not null,
        content text not null,
        author varchar(255) not null,
        dynasty char(10) not null
    )engine = myisam, charset=utf8;
    """
    sql2 = """
    create table poet (
        id int(11) not null primary key auto_increment,
        name varchar(255) not null,
        intro text default null,
        dynasty char(10) not null
    )engine = myisam, charset=utf8;
    """
    cursor.execute(sql1)
    cursor.execute(sql2)

    for dir_dynasty in os.listdir(dir_top):
        path_dynasty = os.path.join(dir_top, dir_dynasty)

        for dir_file in os.listdir(path_dynasty):
            path_file = os.path.join(path_dynasty, dir_file)
            f = open(path_file, 'r+', encoding='utf-8')
            text_raw = json.load(f)
            f.close()
            try:
                #插入poet表中
                r1 = re.compile("\r\n|\n\r|\n|\r")

                cursor = db.cursor()
                poet_result= []
                poet_result.append(text_raw["author"])
                poet_result.append(text_raw["intro"])
                poet_result.append(dir_dynasty)
                query_sql = "select id from poet where name=%s and intro=%s and dynasty=%s"
                if(cursor.execute(query_sql,poet_result) == 0):#如果没有查询到，插入
                    inesrt1 = "insert into poet(name, intro, dynasty) values (%s, %s, %s)"
                    cursor.execute(inesrt1, poet_result)

                cursor.execute(query_sql, poet_result)
                poet_id = cursor.fetchall()[0]
                #取出查询到的结果
                for item in text_raw["items"]:
                #插入poerty表中
                    poetry_result=[]
                    poetry_result.append(poet_id)
                    poetry_result.append(item["title"])
                    content = "<br>".join(r1.split(item["content"]))
                    poetry_result.append(content)
                    poetry_result.append(text_raw["author"])
                    poetry_result.append(dir_dynasty)
                    inesrt2 = "insert into poetry(author_id,title,content,author,dynasty) values (%s, %s, %s,%s, %s)"
                    cursor.execute(inesrt2, poetry_result)

                    print("已处理：" + text_raw["author"] + ":" + item["title"])
            except Exception as e:
                print(str(e))
                break
    cursor.close()
    print("DONE!!!")


if __name__ == "__main__":
    main()
