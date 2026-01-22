# price_data_collection.py 使用说明

## 1. 功能介绍

`price_data_collection.py` 是一个用于从 Baostock API 抓取 A 股股票价格数据的脚本。该脚本能够自动获取指定时间段内的股票代码、名称、行业信息和历史 K 线数据，并将数据保存为 CSV 文件。

## 2. 依赖库

- pandas
- baostock
- datetime

## 3. 脚本结构

### 3.1 核心类

#### `A_Stocks_DataCollection`
- **功能**：A 股数据收集类，用于统一管理和执行数据收集任务
- **初始化参数**：
  - `start_date`：开始日期，格式为 "YYYY-MM-DD"
  - `end_date`：结束日期，格式为 "YYYY-MM-DD"
  - `current_date`：当前日期，格式为 "YYYY-MM-DD"
  - `stocks_num`：股票数量限制，默认值为 10000

### 3.2 主要方法

#### `get_sz50_stocks()`
- **功能**：获取上证 50 指数成分股列表
- **返回值**：包含股票代码和名称的数据框
- **说明**：从 `../llm_factor/CSMD50.csv` 文件读取上证 50 成分股代码，与所有股票列表合并后返回

#### `get_data()`
- **功能**：执行完整的数据收集流程
- **流程**：
  1. 调用 `get_sz50_stocks()` 获取上证 50 成分股
  2. 调用 `get_stock_code_industry()` 获取股票行业信息
  3. 调用 `get_history_k_data()` 获取历史 K 线数据

#### `get_new_data()`
- **功能**：获取指定日期的新数据
- **流程**：
  1. 调用 `get_stocks_code_name()` 获取所有股票代码和名称
  2. 调用 `get_stock_code_industry()` 获取股票行业信息
  3. 调用 `get_history_k_data()` 获取指定日期的 K 线数据

#### `get_stocks_code_name()`
- **功能**：获取所有股票代码和名称
- **返回值**：包含股票代码和名称的数据框
- **说明**：使用 Baostock API 的 `query_all_stock()` 方法获取

#### `get_stock_code_industry(result)`
- **功能**：获取股票行业信息
- **参数**：
  - `result`：包含股票代码的数据框
- **返回值**：包含行业信息的数据框
- **说明**：使用 Baostock API 的 `query_stock_industry()` 方法获取，与输入数据框合并后返回

#### `get_history_k_data(start_date, end_date, result)`
- **功能**：获取历史 K 线数据
- **参数**：
  - `start_date`：开始日期
  - `end_date`：结束日期
  - `result`：包含股票代码和行业信息的数据框
- **返回值**：无直接返回值，将数据保存到 `../data/A_Stocks_Data/{code}.csv` 文件中
- **说明**：使用 Baostock API 的 `query_history_k_data_plus()` 方法获取 K 线数据

#### `previous_date()`
- **功能**：计算当前日期的前一天
- **返回值**：前一天日期字符串，格式为 "YYYY-MM-DD"

## 4. 输入输出

### 4.1 输入

- **配置参数**：
  - `start_date`：开始日期
  - `end_date`：结束日期
  - `current_date`：当前日期
- **外部文件**：
  - `../llm_factor/CSMD50.csv`：上证 50 成分股列表

### 4.2 输出

- **输出目录**：`../data/A_Stocks_Data/`
- **输出文件**：`{code}.csv`（每个股票一个文件）
- **文件格式**：CSV，编码为 UTF-8-SIG

### 4.3 输出数据格式

| 字段名 | 描述 |
|-------|------|
| date | 日期 |
| code | 股票代码 |
| open | 开盘价 |
| high | 最高价 |
| low | 最低价 |
| close | 收盘价 |
| preclose | 前收盘价 |
| volume | 成交量 |
| amount | 成交额 |
| adjustflag | 复权状态 |
| turn | 换手率 |
| tradestatus | 交易状态 |
| pctChg | 涨跌幅 |
| peTTM | 动态市盈率 |
| pbMRQ | 市净率 |
| psTTM | 市销率 |
| pcfNcfTTM | 市现率 |
| isST | 是否 ST |
| code_name | 股票名称 |
| industry | 行业 |
| industryClassification | 行业分类 |

## 5. 使用方法

### 5.1 准备工作

1. 确保已安装所有依赖库：
   ```bash
   pip install pandas baostock
   ```

2. 确保存在 `../llm_factor/CSMD50.csv` 文件（上证 50 成分股列表）

3. 创建数据输出目录：
   ```bash
   mkdir -p ../data/A_Stocks_Data
   ```

### 5.2 运行脚本

在 `dataset_construction` 目录下运行：

```bash
python price_data_collection.py
```

### 5.3 配置说明

- **日期配置**：在脚本末尾的 `if __name__ == "__main__":` 块中修改以下参数：
  - `start_date`：开始日期，默认为 "2019-01-01"
  - `end_date`：结束日期，默认为 "2024-12-18"
  - `current_date`：当前日期，默认为 "2024-12-19"

- **数据范围选择**：
  - 目前默认使用上证 50 成分股（通过 `get_sz50_stocks()` 方法）
  - 如需获取所有股票数据，可以取消注释 `get_data()` 方法的另一个实现（第 26-29 行），并注释掉当前实现（第 21-24 行）

- **数据类型选择**：
  - 调用 `get_data()` 获取历史数据
  - 调用 `get_new_data()` 获取指定日期的新数据

## 6. 注意事项

1. **Baostock API 限制**：Baostock API 可能有访问频率限制，建议不要过于频繁运行脚本
2. **网络稳定性**：确保网络连接稳定，避免因网络问题导致数据获取失败
3. **文件路径**：脚本中使用了相对路径，确保在正确的目录下运行
4. **日期格式**：确保输入的日期格式为 "YYYY-MM-DD"
5. **输出目录**：确保输出目录 `../data/A_Stocks_Data/` 存在，否则会导致文件保存失败

## 7. 运行流程

1. 初始化 `A_Stocks_DataCollection` 类，设置日期参数
2. 调用 `get_data()` 或 `get_new_data()` 方法开始数据收集
3. 登录 Baostock API
4. 获取股票代码和名称
5. 获取股票行业信息
6. 获取历史 K 线数据
7. 将数据保存到 CSV 文件
8. 退出 Baostock API

## 8. 常见问题

### 8.1 登录失败

- **原因**：可能是网络问题或 Baostock API 服务异常
- **解决方法**：检查网络连接，稍后重试

### 8.2 数据获取为空

- **原因**：可能是日期格式错误或该日期无交易数据
- **解决方法**：检查日期格式，确保日期为交易日

### 8.3 文件保存失败

- **原因**：可能是输出目录不存在或权限问题
- **解决方法**：确保输出目录存在，检查文件权限

## 9. 扩展建议

1. 可以添加更多指数成分股的支持（如沪深 300、中证 500 等）
2. 可以实现增量更新功能，只获取新增数据
3. 可以添加数据清洗和预处理功能
4. 可以实现多线程或异步数据获取，提高效率
5. 可以添加数据质量检查功能

## 10. 示例输出

### 输出文件示例（../data/A_Stocks_Data/600000.csv）

```csv
date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST,code_name,industry,industryClassification
2019-01-02,sh.600000,12.41,12.65,12.35,12.60,12.39,155603410,1943457856.0,3,0.241632,1,1.695,6.1167,0.8204,1.7322,2.9173,0,浦发银行,银行业,金融业
2019-01-03,sh.600000,12.53,12.68,12.50,12.58,12.60,93918092,1179820032.0,3,0.145491,1,-0.1587,6.107,0.819,1.7292,2.9121,0,浦发银行,银行业,金融业
...
```

## 11. 代码修改建议

### 11.1 改进异常处理

当前代码中缺乏完整的异常处理机制，建议添加 try-except 块来处理可能的异常，如网络错误、API 错误等。

### 11.2 增加日志记录

建议添加日志记录功能，记录数据收集过程中的关键信息和错误，便于调试和监控。

### 11.3 优化登录逻辑

当前代码中每个方法都单独登录和退出 Baostock API，建议在类的初始化和销毁时统一处理登录和退出。

### 11.4 增加进度显示

对于大量股票的数据收集，可以添加进度显示功能，让用户了解数据收集的进度。