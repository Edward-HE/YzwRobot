# -*- coding:utf-8 –*-


# 导入pandas
import os

import pandas as pd

from yzw.settings import CSV_FILE_PATH


def csv_to_xlsx(file, to_file):
    data_csv = pd.read_csv(file, encoding='gbk', sep=',')
    data_csv.to_excel(to_file, sheet_name='yzw', index=False)


csv_file_list = []


# 获取路径下的png文件
def get_all_filepath(dir):
    parents = os.listdir(dir)
    for parent in parents:
        child = os.path.join(dir, parent)
        if os.path.isdir(child):
            get_all_filepath(child)
        else:
            suffix = os.path.splitext(child)[1]
            # print(suffix)
            if suffix == ".csv":
                csv_file_list.append(child)


# 主函数
def sub_main(csv_file):
    csv_path = os.getcwd() if CSV_FILE_PATH == '.' else CSV_FILE_PATH
    csv_path = os.path.abspath(os.path.join(csv_path, ".."))
    print(csv_file)
    source = os.path.join(csv_path, csv_file)
    print(source)
    # 目标文件路径
    j_mid = str(source).replace(".csv", "")  # 将csv文件名中的.csv后缀去掉
    ob = j_mid + ".xlsx"

    csv_to_xlsx(source, ob)
    print("从 csv 数据转换为 excel 数据", ob)


# 主函数
def main():
    # 源文件路径
    csv_path = os.getcwd() if CSV_FILE_PATH == '.' else CSV_FILE_PATH
    csv_path = os.path.abspath(os.path.join(csv_path, ".."))
    print(csv_path)
    get_all_filepath(csv_path)
    csv_file = csv_file_list[0]
    print(csv_file)
    source = os.path.join(csv_path, csv_file)
    print(source)
    # 目标文件路径
    j_mid = str(source).replace(".csv", "")  # 将csv文件名中的.csv后缀去掉
    ob = j_mid + ".xlsx"

    csv_to_xlsx(source, ob)
    print("从 csv 数据转换为 excel 数据", ob)


if __name__ == '__main__':
    main()
