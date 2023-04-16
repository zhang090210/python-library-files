# 基于Python3.8.10开发
#encoding：utf-8

import sqlite3 #用于对sqlite数据库的操作
import os

import traceback # 用于获取报错信息及发出报错警告
import linecache

class userError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# 输出sqlite插件或数据库版本等信息
class sqlite_info:
    def module_version():
        mv_dict = {}
        mv_dict['version'] = sqlite3.version
        mv_dict['version_info'] = sqlite3.version_info
        for key, value in mv_dict.items():
            print(key+":",value)
        return mv_dict
    def db_version():
        dv_dict = {}
        dv_dict['version'] = sqlite3.sqlite_version
        dv_dict['version_info'] = sqlite3.sqlite_version_info
        for key, value in dv_dict.items():
            print(key+":",value)
        return dv_dict

# 对于数据库的操作类
class db:
    # 创建一个sqlite数据库并返回"cun"和"cur"
    def new(db_name="example.db", new_directory=os.getcwd(), memory=False):
        path_str = os.path.join(new_directory,db_name)
        if memory == True:
            path_str = ":memory:"
        elif db_name[-2:-1] != ".db":
            path_str += ".db"
        
        con = sqlite3.connect(path_str)

        cur = con.cursor()
        print("\ncreate db successful!\n")
        return con,cur


# 对于数据表的操作类
class table:

    # 用于定义此类中多函数重复使用的参数
    def __init__(self, con, cur):
        self.con = con
        self.cur = cur

    # 用于结束时关闭数据库并释放对象占用内存
    def __del__(self):
        con.commit()
        con.close()

    # 用于新建表单
    def new(table_header:dict, table_name="example"):
        if not isinstance(table_header, dict):
            raise userError("对于表头名称和数据类型，请使用字典类型，格式为‘{表头名称:类型}’")
        
        create_str = f"create table {table_name}\n("
        for key, value in table_header.items():
            create_str += f"{key} {value},\n"
        
        create_str = create_str[0:-4]
        create_str += ");"
        
        cur.execute(create_str)
        print ("\ncreate table successful!\n")
        
    # 用于获取指定表单的所有列名称
    def get_col_name(table_name):
        cursor = cur.execute(f"SELECT * from {table_name}")
        name_lst = [tuple[0] for tuple in cur.description]
        print("column name:\n"+"\t".join(name_lst)+"\n")
        return name_lst
    
    # 用于向指定数据表内插入数据
    def insert(content:dict, table_name:str):
        if not isinstance(content, dict):
            raise userError("插入内容参数请使用字典类型 格式为：{列名:参数值}")
        
        insert_str = f"insert into {table_name}"
        key_str = " ("
        value_str = " values ("

        for key, value in content.items():
            key_str += f"{key},"
            value_str += f"{value},"
        key_str = key_str[:-1] + ")"
        value_str = value_str[:-1] + ")"
        insert_str += key_str + value_str
        cur.execute(insert_str)

        print("\n"+insert_str)
        print(f"insert into {table_name} successful!\n")

    # 用于获取数据或指定数据行
    def select(table_name:str, culumn:list=["*"], *condition_list:list):
        column_str = ""
        for i in culumn:
            column_str += i

        if str(condition_list) != "()":  # 当存在查询条件时运行if
            condition_str = "where ("
            for i in condition_list:
                condition_str += i
                condition_str += " and "
            condition_str = condition_str[:-5] + ")"
            select_str = f"select {column_str} from {table_name} {condition_str}"
        else:  # 没有查询条件时运行else
            select_str = f"select {column_str} from {table_name}"
        
        cursor = cur.execute(select_str)
        result = cursor.fetchall() #获取所有数据

        result_pri = []
        for i in result:
            cache_str = str(i)
            result_pri.append(cache_str)
        print("\n"+select_str)
        print("select successful!  result:\n\t"+"\t".join(result_pri)+"\n")
        return result

        
if __name__ == "__main__":
    table_header = {"test1":"int"}
    ini_db = db.new("test.db", memory=True)
    con, cur = ini_db[0], ini_db[1]

    table.new(table_name="test_table", table_header=table_header)
    culumn_name = table.get_col_name(table_name="test_table")

    content = {culumn_name[0]:12345678}
    table.insert(content, table_name="test_table")
    table.insert({culumn_name[0]:1234678}, table_name="test_table")
    condition_lst = ["12345678", "1234678"]
    table.select("test_table", "test1", *condition_lst)