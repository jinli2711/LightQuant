# model 模块 API

本章节详细说明 LightQuant 项目 `model` 目录下所有预测模型的 API 接口。每个模型都继承自 PyTorch 的 `nn.Module` 类，遵循标准的 PyTorch 模型定义规范。

## 模型基类

所有模型类都继承自 `torch.nn.Module`，具有以下共同特征：构造函数 `__init__` 定义网络结构；`forward` 方法定义前向传播逻辑；`get_model` 类方法用于获取模型实例（部分模型支持）。

### 通用参数说明

以下是模型构造函数中的通用参数：input_size 输入特征数量，默认 5（对应 OHLC 五个价格）；hidden_size 隐藏层大小，默认 64；num_layers 网络层数，默认 2；output_size 输出大小，默认 1（预测一个值）；dropout Dropout 比率，默认 0.2；batch_first 设置输入张量的 batch 维度位置，默认 True。

## LSTM.py

标准长短期记忆网络模型。

类签名：
```python
class LSTM(nn.Module)
```

构造函数参数：
- input_size (int)：输入特征数，默认为 5
- hidden_size (int)：隐藏层大小，默认为 64
- num_layers (int)：LSTM 层数，默认为 2
- output_size (int)：输出大小，默认为 1
- dropout (float)：Dropout 比率，默认为 0.2
- batch_first (bool)：True 表示输入为 (batch, seq, feature)，默认为 True

前向传播：
```python
def forward(self, x)
```

输入参数：
- x (torch.Tensor)：输入张量，形状为 (batch, seq_len, input_size)

返回值：
- output (torch.Tensor)：输出张量，形状为 (batch, output_size)

网络结构：
- LSTM 层：input_size -> hidden_size，num_layers 层，带 dropout
- BatchNorm1d 层：对隐藏层输出进行批归一化
- 线性层：hidden_size -> output_size
- Sigmoid 激活层：将输出映射到 (0, 1) 区间

## BiLSTM.py

双向长短期记忆网络模型。

类签名：
```python
class BiLSTM(nn.Module)
```

构造函数参数：
- input_size (int)：输入特征数，默认为 5
- hidden_size (int)：隐藏层大小，默认为 64
- num_layers (int)：LSTM 层数，默认为 2
- output_size (int)：输出大小，默认为 1
- dropout (float)：Dropout 比率，默认为 0.2
- batch_first (bool)：输入格式，默认为 True

前向传播：
```python
def forward(self, x)
```

输入参数：
- x (torch.Tensor)：输入张量，形状为 (batch, seq_len, input_size)

返回值：
- output (torch.Tensor)：输出张量，形状为 (batch, output_size)

网络结构：
- 双向 LSTM 层：input_size -> hidden_size * 2（双向拼接）
- BatchNorm1d 层：对隐藏层输出进行批归一化
- 线性层：hidden_size * 2 -> output_size
- Sigmoid 激活层

特点：
双向 LSTM 同时利用过去和未来的上下文信息，在序列标注等任务中效果更好。

## ALSTM.py

注意力增强 LSTM 模型。

类签名：
```python
class ALSTM(nn.Module)
```

构造函数参数：
- input_size (int)：输入特征数，默认为 5
- hidden_size (int)：隐藏层大小，默认为 64
- num_layers (int)：LSTM 层数，默认为 2
- output_size (int)：输出大小，默认为 1
- dropout (float)：Dropout 比率，默认为 0.2
- attention_size (int)：注意力机制的大小，默认为 64
- batch_first (bool)：输入格式，默认为 True

前向传播：
```python
def forward(self, x)
```

输入参数：
- x (torch.Tensor)：输入张量，形状为 (batch, seq_len, input_size)

返回值：
- output (torch.Tensor)：输出张量，形状为 (batch, output_size)

网络结构：
- LSTM 层：提取序列特征
- 注意力层：对 LSTM 输出进行注意力加权
- BatchNorm1d + 线性层 + Sigmoid

特点：
注意力机制使模型能够关注输入序列中最相关的部分，提高模型的表达能力。

## Adv_LSTM.py

对抗训练 LSTM 模型。

类签名：
```python
class AdvLSTM(nn.Module)
```

构造函数参数：
- input_size (int)：输入特征数，默认为 5
- hidden_size (int)：隐藏层大小，默认为 64
- output_size (int)：输出大小，默认为 1
- attention_size (int)：注意力机制的大小，默认为 64
- perturbation_size (float)：对抗扰动大小，默认为 0.1
- epsilon (float)：对抗训练参数，默认为 0.1

前向传播：
```python
def forward(self, x)
```

输入参数：
- x (torch.Tensor)：输入张量，形状为 (batch, seq_len, input_size)

返回值：
- output (torch.Tensor)：输出张量，形状为 (batch, output_size)

特点：
引入对抗训练技术，通过在输入上添加微小扰动来增强模型的鲁棒性。对抗训练已被证明可以有效提升模型的泛化能力。

## BiGRU.py

双向门控循环单元模型。

类签名：
```python
class BiGRU(nn.Module)
```

构造函数参数：
- input_size (int)：输入特征数，默认为 5
- hidden_size (int)：隐藏层大小，默认为 64
- num_layers (int)：GRU 层数，默认为 2
- output_size (int)：输出大小，默认为 1
- dropout (float)：Dropout 比率，默认为 0.2
- batch_first (bool)：输入格式，默认为 True

网络结构与 BiLSTM 类似，但使用 GRU 作为基础单元。GRU 相比 LSTM 参数更少，训练速度更快，在某些任务上效果相当。

## DTML.py

动态时间记忆网络模型。

类签名：
```python
class DTML(nn.Module)
```

构造函数参数：
- input_size (int)：输入特征数，默认为 7（含时间特征）
- hidden_size (int)：隐藏层大小，默认为 64
- num_layers (int)：网络层数，默认为 2
- n_heads (int)：注意力头数，默认为 4

前向传播：
```python
def forward(self, x)
```

输入参数：
- x (torch.Tensor)：输入张量，形状为 (batch, n_stocks, seq_len, input_size)

返回值：
- output (torch.Tensor)：输出张量，形状为 (batch, n_stocks)

特点：
专门设计用于多股票联合建模，通过跨股票的信息交互捕捉股票间的关联关系。每次训练同时处理多只股票的数据。

## SCINet.py

采样交叉交互网络模型。

类签名：
```python
class SCINet(nn.Module)
```

构造函数参数：
- input_len (int)：输入序列长度，默认为 90
- pred_len (int)：预测长度，默认为 7
- input_dim (int)：输入特征维度，默认为 8
- hidden_dim (int)：隐藏层维度，默认为 64
- SCINet_Layers (int)：SCINet 层数，默认为 3
- kernel_size (int)：卷积核大小，默认为 3
- dropout (float)：Dropout 比率，默认为 0.5

前向传播：
```python
def forward(self, x)
```

输入参数：
- x (torch.Tensor)：输入张量，形状为 (batch, input_len, input_dim)

返回值：
- output (torch.Tensor)：输出张量，形状为 (batch, pred_len)

特点：
通过采样和交叉交互机制捕捉时间序列中的复杂模式，特别适合长时间序列预测任务。

## StockNet.py

股票预测网络模型。

类签名：
```python
class StockNet(nn.Module)
```

构造函数参数：
- price_input_size (int)：价格特征数，默认为 5
- news_input_size (int)：新闻嵌入维度，默认为 768
- hidden_size (int)：隐藏层大小，默认为 128
- output_size (int)：输出大小，默认为 1
- dropout (float)：Dropout 比率，默认为 0.2

前向传播：
```python
def forward(self, price_x, news_x)
```

输入参数：
- price_x (torch.Tensor)：价格特征，形状为 (batch, seq_len, price_input_size)
- news_x (torch.Tensor)：新闻嵌入，形状为 (batch, seq_len, news_input_size)

返回值：
- output (torch.Tensor)：预测概率，形状为 (batch, 1)

特点：
专门设计用于多模态股票预测，通过独立的编码器处理价格和新闻数据，然后进行融合和预测。

## HAN.py

层级注意力网络模型。

类签名：
```python
class HAN(nn.Module)
```

构造函数参数：
- price_input_size (int)：价格特征数，默认为 5
- news_input_size (int)：新闻嵌入维度，默认为 768
- hidden_size (int)：隐藏层大小，默认为 128
- attention_size (int)：注意力层大小，默认为 128
- output_size (int)：输出大小，默认为 1
- dropout (float)：Dropout 比率，默认为 0.1
- pretrained_model (str)：预训练模型名称，默认为 'yiyanghkust/finbert-pretrain'

前向传播：
```python
def forward(self, price_x, news_x)
```

输入参数：
- price_x (torch.Tensor)：价格特征，形状为 (batch, seq_len, price_input_size)
- news_x (torch.Tensor)：新闻嵌入，形状为 (batch, days, max_news, news_input_size)

返回值：
- output (torch.Tensor)：预测概率，形状为 (batch, 1)

网络结构：
- 价格编码器：使用 LSTM 编码价格序列
- 新闻编码器：使用层级注意力机制编码新闻（新闻内注意力 + 新闻间注意力）
- 融合层：拼接价格和新闻表示
- 预测层：全连接 + Sigmoid

特点：
层级注意力网络能够分别关注重要的新闻和重要的词语，适合处理多日多新闻的复杂场景。

## PEN.py

预训练金融模型。

类签名：
```python
class PEN(nn.Module)
```

构造函数参数：
- pretrained_model (str)：预训练模型路径或名称，默认为 'yiyanghkust/finbert-pretrain'
- price_input_size (int)：价格特征数，默认为 5
- hidden_size (int)：隐藏层大小，默认为 128
- output_size (int)：输出大小，默认为 1
- dropout (float)：Dropout 比率，默认为 0.3
- freeze_bert (bool)：是否冻结 BERT 参数，默认为 True

前向传播：
```python
def forward(self, price_x, news_x)
```

输入参数：
- price_x (torch.Tensor)：价格特征，形状为 (batch, seq_len, price_input_size)
- news_x (torch.Tensor)：新闻文本 token IDs，形状为 (batch, days, max_tokens)

返回值：
- output (torch.Tensor)：预测概率，形状为 (batch, 1)

特点：
使用预训练的金融领域 BERT 模型（如 FinBERT）编码新闻文本，结合价格特征进行预测。能够充分利用预训练语言模型的知识。

## GAN_LSTM.py

生成对抗网络 LSTM 模型。

类签名：
```python
class GAN_LSTM(nn.Module)
```

特点：
结合生成对抗网络的思想，通过对抗训练提升 LSTM 的性能。模型包含生成器和判别器两个部分，通过对抗性训练增强模型的表达能力。

## multi_model.py

多模型管理模块。

类签名：
```python
class MultiModel
```

功能说明：
提供统一接口加载和管理多个模型，简化模型选择和切换过程。

### get_model

获取指定名称的模型实例。

函数签名：
```python
def get_model(model_name, **kwargs)
```

参数说明：
- model_name (str)：模型名称
- **kwargs：模型构造参数

返回值：
- model (nn.Module)：模型实例

支持获取的模型包括：lstm、bi_lstm、alstm、adv_lstm、bigru、dtml、scinet、StockNet、han、pen。

## 模型使用示例

### 基本使用流程

```python
import torch
from model.LSTM import LSTM

# 创建模型实例
model = LSTM(
    input_size=5,
    hidden_size=128,
    num_layers=2,
    output_size=1,
    dropout=0.2
)

# 移动到 GPU（如果可用）
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# 前向传播
batch_size = 64
seq_len = 7
input_tensor = torch.randn(batch_size, seq_len, 5).to(device)
output = model(input_tensor)
print(output.shape)  # torch.Size([64, 1])
```

### 多模态模型使用

```python
from model.HAN import HAN

# 创建多模态模型
model = HAN(
    price_input_size=5,
    news_input_size=768,
    hidden_size=128,
    attention_size=128,
    output_size=1
)

# 多输入前向传播
price_input = torch.randn(32, 7, 5)  # (batch, days, price_features)
news_input = torch.randn(32, 5, 10, 768)  # (batch, days, news_count, embed_dim)
output = model(price_input, news_input)
```

### 模型保存和加载

```python
# 保存模型权重
torch.save(model.state_dict(), 'model.pth')

# 加载模型权重
model.load_state_dict(torch.load('model.pth'))
model.eval()  # 设置为评估模式
```
