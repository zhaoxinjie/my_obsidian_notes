---
type: synthesis
status: active
created: 2026-08-13
updated: 2026-08-13
source_count: 1
tags:
  - synthesis
  - llm-training
  - learning-path
  - nanochat
---
# nanochat 架构与学习路径

## 学习目标
学习 nanochat 最值得争取的结果，不是“把所有代码看完”，而是获得三种能力：

1. 能画出一个 LLM 从原始文本到 chat completion 的完整数据流。
2. 能解释一次实验的模型、数据、优化、精度和评测配置。
3. 能做一个小改动，并用正确指标判断它是否有效、代价是什么。

## 一张架构地图

```text
runs/*.sh（实验配方）
        │
        ├── tokenizer ── tok_train / tok_eval
        │                    │
        │               tokenizer.py
        │
        ├── pretrain ─── base_train / base_eval
        │                    │
        │        dataset + dataloader + GPT + optimizer
        │                    │
        │               base checkpoint
        │
        ├── post-train ─ chat_sft ── [可选 chat_rl]
        │                    │
        │             tasks + conversation mask
        │                    │
        │               chat checkpoint
        │
        └── eval/use ── chat_eval / chat_cli / infer_bench
                             │
                     Engine + KV cache + tool use
```

## 推荐阅读顺序

### 第一阶段：先跑通并建立全局地图

阅读顺序：
1. `README.md`
2. `runs/runcpu.sh`
3. `runs/speedrun.sh`

先回答：
- 一次端到端训练有哪些阶段？
- 每个阶段输入、输出什么 artifact？
- base checkpoint 如何变成 chat checkpoint？
- 哪些步骤是学习必须，哪些只是 H100 speedrun 优化？

如果只有 Mac 或 CPU，先跑 `runcpu.sh`。目标是观察数据、tokenizer、checkpoint、评测和生成如何衔接，不追求模型能力。

### 第二阶段：理解最小 Transformer 主干

主读 `nanochat/gpt.py`，但按这个顺序：
1. `GPTConfig`
2. `Block`
3. `CausalSelfAttention`
4. `MLP`
5. `GPT.forward`
6. `setup_optimizer`
7. FLOPs 和参数统计

第一遍主动忽略 FP8、value embedding、smear、backout、滑窗细节。先手写 tensor shape：

```text
token ids (B,T)
→ embedding (B,T,C)
→ q/k/v (B,T,H,D)
→ attention output (B,T,C)
→ MLP (B,T,C)
→ logits (B,T,V)
→ next-token cross entropy
```

完成标准：能解释 causal attention 为什么不能看未来 token，训练为什么可并行，而自回归 decode 为什么逐 token 进行。

### 第三阶段：追踪预训练的一次 step

主读：
1. `scripts/base_train.py`
2. `nanochat/dataloader.py`
3. `nanochat/optim.py`
4. `nanochat/checkpoint_manager.py`

沿一批数据追踪：

```text
Parquet document
→ BPE token ids + BOS
→ best-fit packed x/y
→ model(x,y)
→ cross entropy
→ backward
→ gradient accumulation / DDP
→ MuonAdamW step
→ BPB / CORE / checkpoint
```

重点理解四个量：device batch、total batch tokens、gradient accumulation steps、world size。它们共同决定一次 optimizer step 实际消费多少 token。

### 第四阶段：理解 post-training 如何改变行为

主读：
1. `nanochat/tokenizer.py::render_conversation`
2. `tasks/common.py`
3. `scripts/chat_sft.py`
4. `scripts/chat_eval.py`

把注意力放在：
- 角色与工具特殊 token 如何编码对话协议。
- 为什么只对 assistant token 计算 loss。
- SmolTalk、MMLU、GSM8K 在 mixture 中分别教什么。
- categorical eval 为什么可以直接比较选项 logits，generative eval 为什么必须生成后判分。

完成标准：能新增一个小 task，定义 conversation 渲染和 evaluate/reward，并把它加入训练或评测。

### 第五阶段：理解推理系统

主读：
1. `nanochat/engine.py`
2. `tests/test_engine.py`
3. `scripts/infer_bench.py`

重点理解 prefill、decode 和 KV cache：prefill 一次处理 prompt；decode 每步只输入最新 token，复用历史 K/V。再观察 GQA 和 sliding window 如何减少 KV 存储与读取。

工具调用可作为第二遍内容：Engine 通过 `<|python_start|>` / `<|python_end|>` token 驱动一个小状态机，将计算器结果重新注入生成序列。这能连接到 [[wiki/concepts/工具|工具（tool）]] 与 [[wiki/concepts/测试时计算|测试时计算]]。

### 第六阶段：最后再看研究优化

再研究这些高阶主题：
- scaling law 与单一 depth 旋钮
- muP 风格超参数迁移
- Muon 与 AdamW 参数分工
- Flash Attention / FP8 / `torch.compile`
- value embedding、smear、backout、logit softcap
- `chat_rl.py` 的简化 policy gradient

顺序很重要：这些是“为什么更快或更好”的优化，不是理解端到端系统的前置条件。

## 四周学习计划

### 第 1 周：闭环与模型
- 跑 CPU/MPS 最小流程，记录生成目录和 checkpoint。
- 画出 `speedrun.sh` 流程图。
- 阅读 `gpt.py` 主干并手写所有关键 tensor shape。
- 实验：把 depth 或 sequence length 改小，观察参数量、速度和 loss。

### 第 2 周：数据与训练
- 阅读 tokenizer、dataloader 和 base train loop。
- 打印一个文档的原文、token、packed x/y。
- 算清一次 optimizer step 的 token 数。
- 实验：比较不同 vocab size 或 batch/gradient accumulation 设置对 BPB、吞吐、显存的影响。

### 第 3 周：SFT、评测与推理
- 可视化一条 conversation 的 token 和 loss mask。
- 跑一个小 SFT，比较 base 与 chat checkpoint 的输出。
- 阅读 KV cache，并用测试确认 cached/naive generation 一致。
- 实验：比较 temperature、top-k、context length 对输出和 decode 性能的影响。

### 第 4 周：做一次真正的研究迭代
- 选一个单变量改动，例如 window pattern、数据 mixture、一个 task、激活函数或 tokenizer 配置。
- 先写假设和预期影响。
- 固定预算运行 baseline 与 candidate，至少记录 BPB、CORE/ChatCORE、tokens/sec、MFU、VRAM。
- 分开报告能力变化与系统成本，不用单次 sample 代替评测。

## 最推荐的三个练习

### 练习 1：给模型增加一种可测能力
参考 GSM8K/MMLU，新增一个极小 task：训练集、conversation renderer、evaluate/reward 和评测命令。它能一次贯通 data → SFT → eval。

### 练习 2：做 KV cache 对照实验
用同一 prompt、temperature=0，比较 naive generation 和 Engine generation 的 token 完全一致性，再测不同 context length 的速度和显存。

### 练习 3：做受控消融
关闭或改变一项模型机制，固定 depth、token budget 和数据，比较 BPB/CORE 与吞吐。重点不是得到新 SOTA，而是练习“假设—实验—证据—结论”的闭环。

## 常见误区
- **从 `base_train.py` 第一行一路读到底。** 文件长且包含大量性能细节；应先由 shell pipeline 建地图，再沿数据流阅读。
- **一开始就训练 d24。** 花钱不能替代理解；先在小模型确认流程和指标。
- **只看 loss。** loss、BPB、下游能力、吞吐和显存回答不同问题。
- **把当前 trick 当标准架构。** nanochat 是活跃研究 baseline，实验性机制需要消融验证。
- **同时改多个变量。** 无法归因，也无法积累可靠知识。
- **只读不运行。** 训练系统中很多关键知识存在于 shape、日志、显存、速度和失败模式里。

## 需要的前置知识
最低限度：
- Python、PyTorch module/autograd/optimizer
- 线性代数中的矩阵乘法与 tensor shape
- softmax、cross-entropy、gradient descent
- Transformer decoder、causal self-attention
- 基本 shell、环境管理与 GPU/显存概念

不需要先掌握：CUDA kernel、分布式训练论文、RLHF 全家桶或 scaling law 推导。遇到相应代码时按需补齐即可。

## 相关页面
- [[wiki/sources/2026-08-13 Karpathy - nanochat|2026-08-13 Karpathy - nanochat]]
- [[wiki/entities/Andrej Karpathy|Andrej Karpathy]]
- [[wiki/concepts/AI评估|AI评估]]
- [[wiki/concepts/测试时计算|测试时计算]]
- [[wiki/concepts/工具|工具（tool）]]
- [[wiki/concepts/软件工程|软件工程]]

