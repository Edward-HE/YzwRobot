def csv_writer(): 
    import csv 
    a = [] 
    dict = student_infos[0] 
    for headers in dict.keys():  
        # 把字典的键取出来,注意不要使用sorted不然会导致键的顺序改变 
        a.append(headers) 
        print(a) 
        header=a
        #把列名给提取出来，用列表形式呈现 
        with open('成绩更新.csv', 'a', newline='', encoding='utf-8') as f: 
            writer = csv.DictWriter(f, fieldnames=header) 
            # 提前预览列名，当下面代码写入数据时，会将其一一对应。 
            writer.writeheader() # 写入列名 
            writer.writerows(student_infos) # 写入数据 
            print("数据已经写入成功！！！") # a表示以“追加”的形式写入，如果是“w”的话，表示在写入之前会清空原文件中的数据 
            # newline是数据之间不加空行 
            # # encoding='utf-8'表示编码格式为utf-8，如果不希望在excel中打开csv文件出现中文乱码的话，将其去掉不写也行。 
            # # 为了不让pycharm里面的CSV文件乱码，我们这里用的参数编码为utf-8 
            # # 而excel文件编码格式是gbk，两者不兼容，建议加上encoding='utf-8’参数。 
            # # 如果不想excel中的csv文件乱码的话，建议将csv文件以记事本的方式打开，另存为ANSI格式即可。
