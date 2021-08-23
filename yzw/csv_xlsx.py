# -*- coding:utf-8 –*-


# 导入pandas
import os

import pandas as pd

from yzw.settings import CSV_FILE_NAME
from yzw.settings import CSV_FILE_PATH


def csv_to_xlsx(file, to_file):
    data_csv = pd.read_csv(file, encoding='gbk', sep=',')
    data_csv.to_excel(to_file, sheet_name='yzw', index=False)


# 主函数
def main():
    # 源文件路径
    csv_path = os.getcwd() if CSV_FILE_PATH == '.' else CSV_FILE_PATH
    csv_file = CSV_FILE_NAME + '.csv'
    source = os.path.join(csv_path, csv_file)
    print(source)
    # 目标文件路径
    j_mid = str(source).replace(".csv", "")  # 将csv文件名中的.csv后缀去掉
    ob = j_mid + ".xlsx"

    csv_to_xlsx(source, ob)
    print("从 csv 数据转换为 excel 数据", ob)


if __name__ == '__main__':
    main()
