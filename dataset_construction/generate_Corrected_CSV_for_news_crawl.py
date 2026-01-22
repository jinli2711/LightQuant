import pandas as pd

# 读取上证50成分股列表
sz50_stocks = pd.read_csv('../llm_factor/CSMD50.csv', encoding='utf-8')

# 重命名列以匹配新闻爬虫脚本的要求
sz50_stocks = sz50_stocks.rename(columns={'code': 'code', 'code_name': 'code_name'})

# 保存为新闻爬虫脚本所需的文件
sz50_stocks[['code', 'code_name']].to_csv('Corrected_CSV_File_Last_Date_Summary.csv', index=False, encoding='utf-8')