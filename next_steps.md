# 后续步骤建议

根据您已经获取到的数据和项目架构，以下是后续的详细步骤建议：

## 1. 数据整理与格式化

首先，将您获取到的数据整理成项目所需的格式：

### 股价数据
- 将 `data\A_Stocks_Data` 目录下的股价数据复制到 `dataset\CSMD50\price` 目录下
- 确保文件名格式与项目一致（建议使用股票简称，如"贵州茅台.csv"）
- 确保CSV文件包含必要的字段：Date, Open, High, Low, Close, Volume等

### 新闻数据
- 将 `news` 目录下的新闻数据整理到 `dataset\CSMD50\news` 目录下
- 按照股票简称创建子目录，如 `dataset\CSMD50\news\贵州茅台`
- 按照日期创建CSV文件，如 `2024-01-01.csv`，包含新闻文本等信息

## 2. 使用LLM从新闻中提取金融因子

运行 `llm_factor\extract_factors.py` 脚本，从新闻文本中提取影响股价的金融因子：

```python
python ./llm_factor/extract_factors.py --model_path <your_model_path> --tokenizer_path <your_tokenizer_path> --dataset CSMD50 --original_news_path ./news --output_news_path ./dataset/CSMD50/news_factors
```

**注意事项**：
- 需要替换 `<your_model_path>` 和 `<your_tokenizer_path>` 为实际的模型路径
- 该脚本使用大语言模型从新闻中提取影响股价的前3个因素

## 3. 生成新闻文本的Word2Vec嵌入

运行 `utils\word2vec.py` 脚本，生成新闻文本的嵌入向量：

```python
python ./utils/word2vec.py --dataset CSMD50 --csv_news_path ./dataset/CSMD50/news --embedding_path ./dataset/CSMD50/news_embedding --local_model_path <your_bert_model_path>
```

**注意事项**：
- 需要替换 `<your_bert_model_path>` 为实际的BERT模型路径
- 该脚本会为每条新闻生成嵌入向量，并按照指定的回溯天数进行聚合

## 4. 数据集处理与分割

运行 `utils\util.py` 脚本，进行数据清洗、分割和标签创建：

```python
python ./utils/util.py --dataset CSMD50
```

该脚本会执行以下操作：
- 统计并填充缺失值（使用线性插值）
- 生成交易日期列表
- 将数据集分割为训练集、验证集和测试集
- 创建标签（基于次日收盘价相对今日收盘价的涨跌）

## 5. 模型训练与评估

运行 `run.py` 脚本，使用单模态（股价）或多模态（股价+新闻）数据进行模型训练和评估：

```python
# 使用多模态数据（推荐）
python run.py --dataset CSMD50 --use_news True --model HAN

# 或使用单模态数据（仅股价）
python run.py --dataset CSMD50 --use_news False --model LSTM
```

**注意事项**：
- 可以选择不同的模型，如LSTM、BiLSTM、ALSTM、Adv-LSTM、SCINet、DTML、StockNet、HAN、PEN等
- 训练结果会保存在 `result\CSMD50` 目录下

## 6. 策略回测

运行回测脚本，评估模型在实际交易中的表现：

```python
python ./backtest/run_backtest.py --dataset CSMD50 --model HAN
```

**注意事项**：
- 回测结果会包含年化收益率、夏普比率、最大回撤等指标
- 可以根据回测结果调整模型参数或策略

## 7. 结果分析与优化

- 查看模型训练和评估结果，分析模型的性能
- 根据结果调整模型参数或尝试不同的模型架构
- 可以尝试使用不同的LLM模型或参数来提取金融因子
- 可以尝试调整新闻嵌入的生成方式或参数

## 注意事项

1. 确保已安装所有依赖：
   ```python
   pip install -r requirements.txt
   # 单独安装PyTorch（根据CUDA版本调整）
   pip install torch==2.4.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

2. 项目使用SwanLab进行实验跟踪，您可以选择修改 `run.py` 中的SwanLab配置，或注释掉相关代码

3. 所有脚本都支持命令行参数，您可以根据需要调整参数值

4. 详细的模型参数说明可以查看各脚本的代码注释

祝您实验顺利！