# backtest 模块 API

本章节详细说明 LightQuant 项目 `backtest` 目录下回测框架的 API 接口，包括回测函数、评估指标和回测运行脚本。

## metrics.py

回测评估指标计算模块，定义了所有回测相关的性能指标计算函数。

### calculate_MDD

计算最大回撤（Maximum Drawdown）。

函数签名：
```python
def calculate_MDD(asset_list)
```

参数说明：
- asset_list (list[float])：资产净值序列，每个元素代表一天的资产价值

返回值：
- MDD (float)：最大回撤值，取值范围为 0 到 1

功能说明：
最大回撤计算公式为：MDD = max((峰值 - 谷值) / 峰值)。该指标衡量策略在最坏情况下从峰值到谷值的跌幅，反映策略的极端风险。

### calculate_Calmar_Ratio

计算 Calmar 比率。

函数签名：
```python
def calculate_Calmar_Ratio(ARR, MDD)
```

参数说明：
- ARR (float)：年化收益率
- MDD (float)：最大回撤

返回值：
- CR (float)：Calmar 比率

功能说明：
Calmar 比率 = ARR / MDD。衡量每单位最大回撤获得的收益，值越高表示风险收益特征越好。

### calculate_IR

计算信息比率（Information Ratio）。

函数签名：
```python
def calculate_IR(asset_list, risk_free_rate=0.03)
```

参数说明：
- asset_list (list[float])：资产净值序列
- risk_free_rate (float)：无风险利率，默认为 0.03（年化）

返回值：
- IR (float)：信息比率

功能说明：
信息比率衡量策略相对于无风险资产的超额收益及其稳定性。计算假设日交易，使用 252 天年化。忽略 NaN 和 Inf 值进行计算。

### calculate_ACC

计算分类准确率。

函数签名：
```python
def calculate_ACC(actual_directions, predicted_directions)
```

参数说明：
- actual_directions (list[int])：真实涨跌方向列表
- predicted_directions (list[int])：预测涨跌方向列表

返回值：
- ACC (float)：准确率，取值范围为 0 到 1

功能说明：
使用 sklearn 的 accuracy_score 计算预测正确的比例。真实值和预测值应为 0 或 1。

### calculate_ARR

计算年化收益率（Annualized Return Rate）。

函数签名：
```python
def calculate_ARR(asset_list)
```

参数说明：
- asset_list (list[float])：资产净值序列

返回值：
- ARR (float)：年化收益率，可能为 NaN

功能说明：
年化收益率计算公式为：ARR = (最终资产 / 初始资产)^(252/天数) - 1。假设一年有 252 个交易日。

### calculate_SR

计算夏普比率（Sharpe Ratio）。

函数签名：
```python
def calculate_SR(asset_list, risk_free_rate=0.01)
```

参数说明：
- asset_list (list[float])：资产净值序列
- risk_free_rate (float)：无风险利率，默认为 0.01（年化）

返回值：
- SR (float)：夏普比率，可能为 NaN

功能说明：
夏普比率计算公式为：SR = (年化收益 - 无风险利率) / 年化波动率。衡量每单位总风险获得的超额收益。

### calculate_cumulative_return

计算累计收益率序列。

函数签名：
```python
def calculate_cumulative_return(asset_list)
```

参数说明：
- asset_list (list[float])：资产净值序列

返回值：
- cumulative_returns (list[float])：累计收益率序列

功能说明：
计算每一天相对于初始资产的累计收益率。首日为 0，之后每一天为 (当日资产 / 初始资产) - 1。

## backtest_single.py

单模型回测模块，提供单个模型的回测功能。

### backtest_normal

普通模型回测函数。

函数签名：
```python
def backtest_normal(dataloader, model, device)
```

参数说明：
- dataloader (DataLoader)：回测数据加载器
- model (nn.Module)：训练好的模型
- device (torch.device)：计算设备

返回值：
- ACC (float)：准确率
- ARR (float)：年化收益率
- SR (float)：夏普比率
- MDD (float)：最大回撤
- CR (float)：Calmar 比率
- IR (float)：信息比率
- Cumulative_Return (list[float])：累计收益率序列

功能说明：
对使用标准数据格式的模型进行回测。策略为：预测值 > 0.5 买入，预测值 <= 0.5 卖出或做空。支持做空交易。

### backtest_dtml

DTML 模型回测函数。

函数签名：
```python
def backtest_dtml(dataloader, model, device, n_stocks)
```

参数说明：
- dataloader (DataLoader)：DTML 数据加载器
- model (nn.Module)：DTML 模型
- device (torch.device)：计算设备
- n_stocks (int)：每组股票数量

返回值：
- ACC_List (list[float])：各股票准确率列表
- ARR_List (list[float])：各股票年化收益率列表
- SR_List (list[float])：各股票夏普比率列表
- MDD_List (list[float])：各股票最大回撤列表
- CR_List (list[float])：各股票 Calmar 比率列表
- IR_List (list[float])：各股票信息比率列表
- Cumulative_Return_List (list[list[float]])：各股票累计收益率序列列表

功能说明：
对 DTML 模型进行回测，分别计算每只股票的性能指标。

### backtest_scinet

SCINet 模型回测函数。

函数签名：
```python
def backtest_scinet(dataloader, model, device)
```

参数说明：
- dataloader (DataLoader)：SCINet 数据加载器
- model (nn.Module)：SCINet 模型
- device (torch.device)：计算设备

返回值：
- ACC (float)：准确率
- ARR (float)：年化收益率
- SR (float)：夏普比率
- MDD (float)：最大回撤
- CR (float)：Calmar 比率
- IR (float)：信息比率
- Cumulative_Return (list[float])：累计收益率序列

功能说明：
对 SCINet 模型进行回测。SCINet 使用不同的预测长度和输入格式。

### backtest_single

主回测函数。

函数签名：
```python
def backtest_single(args)
```

参数说明：
- args (Namespace)：命令行参数

功能说明：
回测的主入口函数。根据模型类型选择对应的回测函数，加载模型权重，遍历测试集股票进行回测，计算并输出各指标的平均值。

支持的模型类型：lstm、bi_lstm、alstm、adv_lstm、dtml、scinet。

## backtest_multi.py

多模型对比回测模块，支持同时对多个模型进行回测对比。

### run_multi_backtest

运行多模型回测对比。

函数签名：
```python
def run_multi_backtest(args, model_list)
```

参数说明：
- args (Namespace)：命令行参数
- model_list (list[str])：模型名称列表

功能说明：
依次对列表中的每个模型进行回测，生成对比结果。结果包括各模型的指标汇总和可视化对比图。

## run_backtest.py

回测运行脚本，提供命令行接口。

### 使用方法

基本命令格式：
```bash
python backtest/run_backtest.py --dataset CSMD50 --model LSTM --use_news False --look_back_window 7 --model_save_folder ./result/CSMD50/model_saved/ --test_price_folder ./dataset/CSMD50/test/price/ --backtest_result_folder ./result/CSMD50/backtest_result/
```

### 命令行参数

数据路径参数：
- dataset：数据集名称，默认 'CSMD50'
- test_price_folder：测试集价格数据路径
- model_save_folder：模型保存路径

模型参数：
- model：模型名称
- look_back_window：回看窗口大小
- use_news：是否使用新闻数据
- input_size：输入特征数
- hidden_size：隐藏层大小
- layers：网络层数
- attention_size：注意力层大小
- perturb perturbation_size：对抗扰动大小
- epsilon：对抗训练参数
- n_stocks：DTML 股票数量
- seq_len：SCINet 序列长度
- pred_len：SCINet 预测长度
- SCINet_Layers：SCINet 层数

运行参数：
- batch_size：批量大小
- useGPU：是否使用 GPU
- GPU_ID：GPU 编号
- backtest_result_folder：回测结果保存路径

### 输出文件

回测完成后生成以下文件：
- {model}.txt：包含各指标平均值的文本文件
- {model}_cumulative_return.csv：包含每日累计收益率的 CSV 文件

## 回测策略细节

### 交易规则

默认回测策略的交易规则如下：初始资金为 10000 元；每次买入或卖出 1 手（100 股）股票；预测值 > 0.5 时买入或持有；预测值 <= 0.5 时卖出或做空；不考虑交易滑点，成交价为当日收盘价；允许做空。

### 收益计算

收益计算基于资产净值序列。每日资产价值计算公式为：资产 = 现金 + 股票数量 × 收盘价。初始资产净值设为 1.0，后续资产净值相对于初始值计算。

### 结果解读

回测结果的解读要点：ACC 反映预测准确程度；ARR 为正表示策略盈利，为负表示亏损；SR 越高表示风险调整后收益越好；MDD 越大表示最大风险越大；CR 综合考虑收益和回撤；IR 表示相对于无风险资产的超额收益能力。
