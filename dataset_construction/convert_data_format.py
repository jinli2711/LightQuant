import pandas as pd
import json
import os
from datetime import datetime
import shutil

def convert_price_data():
    """
    转换股价数据格式
    从 data/A_Stocks_Data 转换到 dataset/CSMD50/price
    """
    print("开始转换股价数据...")
    
    stock_info_path = './Corrected_CSV_File_Last_Date_Summary.csv'
    stock_info = pd.read_csv(stock_info_path, encoding='utf-8')
    
    code_to_name = dict(zip(stock_info['code'], stock_info['code_name']))
    
    source_dir = '../data/A_Stocks_Data'
    target_dir = '../dataset/CSMD50/price'
    
    os.makedirs(target_dir, exist_ok=True)
    
    for filename in os.listdir(source_dir):
        if filename.endswith('.csv'):
            code = filename.replace('.csv', '')
            
            if code not in code_to_name:
                print(f"警告：找不到股票代码 {code} 对应的名称，跳过")
                continue
            
            stock_name = code_to_name[code]
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, f'{stock_name}.csv')
            
            df = pd.read_csv(source_path, encoding='utf-8')
            
            converted_df = pd.DataFrame({
                'Date': df['date'],
                'Open': df['open'],
                'High': df['high'],
                'Low': df['low'],
                'Close': df['close'],
                'Adj Close': df['close'],
                'Volume': df['volume']
            })
            
            converted_df.to_csv(target_path, index=False, encoding='utf-8-sig')
            print(f"已转换股价数据：{filename} -> {stock_name}.csv")
    
    print(f"股价数据转换完成，共处理 {len(os.listdir(source_dir))} 个文件")

def convert_news_data():
    """
    转换新闻数据格式
    从 news 转换到 dataset/CSMD50/news
    """
    print("开始转换新闻数据...")
    
    stock_info_path = './Corrected_CSV_File_Last_Date_Summary.csv'
    stock_info = pd.read_csv(stock_info_path, encoding='utf-8')
    
    code_to_name = dict(zip(stock_info['code'], stock_info['code_name']))
    
    source_dir = '../news'
    target_dir = '../dataset/CSMD50/news'
    
    os.makedirs(target_dir, exist_ok=True)
    
    for filename in os.listdir(source_dir):
        if filename.endswith('.json'):
            code = filename.replace('.json', '')
            
            if code not in code_to_name:
                print(f"警告：找不到股票代码 {code} 对应的名称，跳过")
                continue
            
            stock_name = code_to_name[code]
            source_path = os.path.join(source_dir, filename)
            target_stock_dir = os.path.join(target_dir, stock_name)
            os.makedirs(target_stock_dir, exist_ok=True)
            
            with open(source_path, 'r', encoding='utf-8') as f:
                news_list = json.load(f)
            
            news_by_date = {}
            
            for news in news_list:
                time_str = news['time']
                try:
                    date_str = time_str.split(' ')[0]
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    date_str = date_obj.strftime('%Y-%m-%d')
                except:
                    print(f"警告：无法解析时间格式 {time_str}，跳过该新闻")
                    continue
                
                if date_str not in news_by_date:
                    news_by_date[date_str] = []
                
                news_by_date[date_str].append({
                    'code_name': stock_name,
                    'ticker': code,
                    'created_at': date_str,
                    'text': f"{news['title']}。{news['content']}"
                })
            
            for date_str, news_items in news_by_date.items():
                date_file_path = os.path.join(target_stock_dir, f'{date_str}.csv')
                df = pd.DataFrame(news_items)
                
                if os.path.exists(date_file_path):
                    existing_df = pd.read_csv(date_file_path, encoding='utf-8-sig')
                    df = pd.concat([existing_df, df], ignore_index=True)
                
                df.to_csv(date_file_path, index=False, encoding='utf-8-sig')
            
            print(f"已转换新闻数据：{filename} -> {stock_name}/ (共 {len(news_by_date)} 个日期)")
    
    print(f"新闻数据转换完成，共处理 {len(os.listdir(source_dir))} 个文件")

def main():
    """
    主函数：执行所有数据转换
    """
    print("=" * 60)
    print("开始数据转换流程")
    print("=" * 60)
    
    try:
        convert_price_data()
        print()
        convert_news_data()
        print()
        print("=" * 60)
        print("数据转换全部完成！")
        print("=" * 60)
        print(f"股价数据已保存到：dataset/CSMD50/price/")
        print(f"新闻数据已保存到：dataset/CSMD50/news/")
    except Exception as e:
        print(f"错误：数据转换过程中出现异常")
        print(f"异常信息：{e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()