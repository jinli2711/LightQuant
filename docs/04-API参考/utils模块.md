# utils 模块 API

本章节详细说明 LightQuant 项目 `utils` 目录下所有模块的 API 接口，包括数据加载、预处理、词向量生成和可视化等工具函数。

## price_dataloader.py

价格数据加载模块，提供 PyTorch Dataset 和 DataLoader 的创建函数，支持单模态训练和回测场景。

### load_csv_file

加载单个 CSV 文件并进行标准化处理。

函数签名：
```python
def load_csv_file(csv_file, feature_columns, label_columns)
```

参数说明：
- csv_file (str)：CSV 文件路径
- feature_columns (list[str])：特征列名列表，如 ['Open', 'High', 'Low', 'Close', 'Adj Close']
- label_columns (list[str])：标签列名列表，如 ['Label']

返回值：
- feature (torch.Tensor)：标准化后的特征张量，形状为 (样本数, 特征数)
- label (torch.Tensor)：标签张量，形状为 (样本数,)

功能说明：
读取 CSV 文件，对指定特征列进行标准化处理（减去均值除以标准差），返回特征和标签张量。标准化参数在每个股票数据上独立计算，避免数据泄露。

### split_sequence

将连续序列分割为固定长度的子序列。

函数签名：
```python
def split_sequence(sequence, length)
```

参数说明：
- sequence (torch.Tensor)：输入序列张量
- length (int)：子序列长度

返回值：
- sequences (torch.Tensor)：分割后的子序列张量，形状为 (序列数 - length + 1, length, ...)

功能说明：
将一维或多维序列按照指定长度滑动分割，返回所有子序列。例如，对长度为 100 的序列使用长度 7 分割，得到 94 个子序列。

### standardize_dataframe

对 DataFrame 指定列进行标准化处理。

函数签名：
```python
def standardize_dataframe(dataframe, feature_columns)
```

参数说明：
- dataframe (pd.DataFrame)：输入数据框
- feature_columns (list[str])：需要标准化的列名列表

返回值：
- dataframe (pd.DataFrame)：标准化后的数据框

功能说明：
对指定列计算均值和标准差，然后进行标准化变换：column = (column - mean) / std。变换是原地进行的，直接修改原数据框。

### Normal_Dataset

普通数据集类，继承自 torch.utils.data.Dataset。

类签名：
```python
class Normal_Dataset(Dataset)
```

构造函数参数：
- csv_files (list[str], optional)：CSV 文件路径列表，默认为 []
- look_back_window (int)：回看窗口大小，默认为 1

主要方法：
- __len__()：返回数据集样本数
- __getitem__(idx)：获取指定索引的样本，返回 (feature, label) 元组

功能说明：
加载多个股票的价格数据，标准化后按照回看窗口分割为序列样本。支持批量加载和随机打乱，适用于模型训练和验证。

### Backtest_Dataset

回测专用数据集类，继承自 torch.utils.data.Dataset。

类签名：
```python
class Backtest_Dataset(Dataset)
```

构造函数参数：
- csv_file (str)：股票价格 CSV 文件路径
- look_back_window (int)：回看窗口大小，默认为 7
- feature_columns (list[str], optional)：特征列名列表
- label_column (str)：标签列名，默认为 'Label'

主要方法：
- __len__()：返回数据集样本数
- __getitem__(idx)：获取指定索引的样本，返回 (normalized_seq, raw_seq, label) 元组
- get_dates()：返回样本对应的日期列表

功能说明：
用于回测场景的数据集，除了返回标准化的特征序列外，还返回原始特征序列（用于计算实际收益）和日期信息。

### DTML_Dataset

DTML 模型专用数据集类，继承自 torch.utils.data.Dataset。

类签名：
```python
class DTML_Dataset(Dataset)
```

构造函数参数：
- data_folder (str)：包含股票 CSV 文件的文件夹路径
- look_back_window (int)：回看窗口大小，默认为 7
- n_stocks (int)：每次采样的股票数量，默认为 5

主要方法：
- __len__()：返回数据集 batch 数
- __getitem__(idx)：获取随机采样的股票组，返回 (features, labels) 元组

功能说明：
为 DTML 模型设计的数据集，每次返回多只股票的样本，实现跨股票的联合建模。数据中包含时间特征（星期几、月份）。

### SCINet_Dataset

SCINet 模型专用数据集类，继承自 torch.utils.data.Dataset。

类签名：
```python
class SCINet_Dataset(Dataset)
```

构造函数参数：
- data_folder (str)：包含股票 CSV 文件的文件夹路径
- seq_len (int)：输入序列长度
- pred_len (int)：预测长度

主要方法：
- __len__()：返回数据集样本数
- __getitem__(idx)：获取样本，返回 (features, labels) 元组

功能说明：
为 SCINet 模型设计的数据集，支持变长输入输出。标签为未来 pred_len 天的涨跌方向序列。

### Backtest_SCINet_Dataset

SCINet 模型回测专用数据集类，继承自 torch.utils.data.Dataset。

类签名：
```python
class Backtest_SCINet_Dataset(Dataset)
```

构造函数参数：
- csv_file (str)：股票价格 CSV 文件路径
- seq_len (int)：输入序列长度，默认为 90
- pred_len (int)：预测长度，默认为 7
- feature_columns (list[str], optional)：特征列名列表

主要方法：
- __len__()：返回数据集样本数
- __getitem__(idx)：获取样本，返回 (sequence, raw_close, label) 元组
- get_dates()：返回样本对应的日期列表

功能说明：
SCINet 模型回测专用数据集，除特征序列外还返回收盘价用于计算收益。

### create_dataset

创建数据集的统一接口。

函数签名：
```python
def create_dataset(train_folder=None, val_folder=None, test_folder=None, backtest_file=None, look_back_window=1)
```

参数说明：
- train_folder (str, optional)：训练集文件夹路径
- val_folder (str, optional)：验证集文件夹路径
- test_folder (str, optional)：测试集文件夹路径
- backtest_file (str, optional)：回测文件路径，与文件夹参数互斥
- look_back_window (int)：回看窗口大小

返回值：
根据输入参数返回 (train, val, test) 元组或单个回测数据集

功能说明：
工厂函数，根据输入参数类型和组合返回对应的数据集对象。简化了不同场景下的数据集创建过程。

### create_dataloader

创建 DataLoader 的统一接口。

函数签名：
```python
def create_dataloader(dataset, batch_size=32, shuffle=True, drop_last=False)
```

参数说明：
- dataset (Dataset)：PyTorch Dataset 对象
- batch_size (int)：批量大小，默认为 32
- shuffle (bool)：是否打乱数据，默认为 True
- drop_last (bool)：是否丢弃最后一个不完整批次，默认为 False

返回值：
- dataloader (DataLoader)：PyTorch DataLoader 对象

功能说明：
封装 DataLoader 的创建过程，设置常用的默认参数。

## price_news_dataloader.py

多模态数据加载模块，同时加载价格数据和新闻嵌入数据。

### Multi_Dataset

多模态数据集类，继承自 torch.utils.data.Dataset。

类签名：
```python
class Multi_Dataset(Dataset)
```

构造函数参数：
- csv_files (list[str])：价格数据 CSV 文件路径列表
- news_files (list[str])：新闻嵌入文件路径列表
- look_back_window (int)：回看窗口大小

主要方法：
- __len__()：返回数据集样本数
- __getitem__(idx)：获取样本，返回 (price_feature, news_feature, label) 元组

功能说明：
同时加载价格数据和新闻嵌入数据，确保两者的日期对齐。对齐后的样本包含价格特征、新闻嵌入和标签。

## util.py

通用工具函数模块，包含数据检查、预处理和划分等功能。

### count_null_and_na_values

统计数据集中的空值数量。

函数签名：
```python
def count_null_and_na_values(dataset)
```

参数说明：
- dataset (str)：数据集名称，如 'CSMD50'

功能说明：
扫描数据集中所有 CSV 文件，统计每列的空值（null）和 NA 值数量。输出汇总报告，包含总空值数和每个文件的详细统计。

### linear_interpolation

使用线性插值填补缺失值。

函数签名：
```python
def linear_interpolation(dataset)
```

参数说明：
- dataset (str)：数据集名称，如 'CSMD50'

功能说明：
对数据集中所有 CSV 文件进行缺失值填补。填补顺序为：首先使用线性插值填补中间缺失值，然后使用前向填充填补开头缺失值，最后使用后向填充填补结尾缺失值。处理完成后原地保存文件。

### generate_trading_date_list

生成交易日列表。

函数签名：
```python
def generate_trading_date_list(dataset)
```

参数说明：
- dataset (str)：数据集名称，如 'CSMD50'

功能说明：
从价格数据中提取所有日期，生成交易日列表并保存到文件。列表用于词向量生成等需要交易日信息的场景。

### split_data

划分训练集、验证集和测试集。

函数签名：
```python
def split_data(dataset)
```

参数说明：
- dataset (str)：数据集名称，如 'CSMD50'

功能说明：
按照预设的时间范围划分数据集。默认划分：训练集到 2024-03-14，验证集到 2024-08-07，测试集为之后的数据。自动创建目录结构并复制文件。

### create_label

生成标签列。

函数签名：
```python
def create_label(dataset)
```

参数说明：
- dataset (str)：数据集名称，如 'CSMD50'

功能说明：
根据下一个交易日收盘价与当前收盘价的比较生成标签。Label = 1 if Close(t+1) > Close(t) else 0。在所有划分后的数据集上执行。

## word2vec.py

词向量生成模块，将新闻文本转换为向量表示。

### generate_word2vec_embeddings

生成新闻词向量嵌入。

函数签名：
```python
def generate_word2vec_embeddings(dataset, csv_news_path, embedding_path, local_model_path, trading_date_list)
```

参数说明：
- dataset (str)：数据集名称
- csv_news_path (str)：原始新闻数据路径
- embedding_path (str)：嵌入输出路径
- local_model_path (str)：本地模型路径
- trading_date_list (str)：交易日列表文件路径

功能说明：
遍历所有新闻数据，使用预训练模型生成词向量嵌入。嵌入按股票和日期组织，保存为 .npy 格式。

## news_process.py

新闻数据处理模块。

### process_news

处理单条新闻数据。

函数签名：
```python
def process_news(news_item)
```

参数说明：
- news_item (dict)：包含 time、title、content 的字典

返回值：
- processed_item (dict)：处理后的新闻数据

功能说明：
对新闻进行预处理，包括清理特殊字符、规范化格式等。

### aggregate_news_by_date

按日期聚合新闻。

函数签名：
```python
def aggregate_news_by_date(news_data)
```

参数说明：
- news_data (list[dict])：新闻数据列表

返回值：
- aggregated (dict)：按日期聚合的新闻字典

功能说明：
将多条新闻按日期分组，返回日期到新闻列表的映射。便于进行日级别的分析和建模。

## plot.py

可视化模块，提供回测结果绘图功能。

### plot_cumulative_return

绘制累计收益率曲线。

函数签名：
```python
def plot_cumulative_return(result_file, output_file)
```

参数说明：
- result_file (str)：累计收益率 CSV 文件路径
- output_file (str)：输出图片路径

功能说明：
读取回测结果数据，绘制累计收益率曲线图。图片保存为 PNG 格式。

### plot_comparison

绘制多模型对比图。

函数签名：
```python
def plot_comparison(result_files, output_file, labels)
```

参数说明：
- result_files (list[str])：多个结果文件路径列表
- output_file (str)：输出图片路径
- labels (list[str])：各曲线标签列表

功能说明：
将多个模型的累计收益率曲线绘制在同一张图上进行对比。

## test.py

测试验证模块。

### run_tests

运行安装验证测试。

函数签名：
```python
def run_tests()
```

功能说明：
执行一系列基础测试验证安装是否正确，包括：导入测试、GPU 测试、数据加载测试等。测试通过输出成功信息，失败输出错误信息。
