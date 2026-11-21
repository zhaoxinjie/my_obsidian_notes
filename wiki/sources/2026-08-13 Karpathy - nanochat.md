---
type: source
status: active
created: 2026-08-13
updated: 2026-08-13
tags:
  - source
  - llm-training
  - pytorch
  - nanochat
---
# 2026-08-13 Karpathy - nanochat

## 来源
- 仓库：[karpathy/nanochat](https://github.com/karpathy/nanochat)
- 作者：[[wiki/entities/Andrej Karpathy|Andrej Karpathy]] 及社区贡献者
- 定位：可在单个 GPU 节点上运行的端到端 LLM 实验 harness
- 阅读版本：`master` commit [`92d63d4`](https://github.com/karpathy/nanochat/commit/92d63d4e8bb4df75c3b71618f31ddde2378b2bcd)，2026-07-03
- 阅读日期：2026-08-13

## 一句话总结
nanochat 的重点不是发明一种全新的 Transformer，而是用一套小而完整的代码，把 tokenizer、预训练、SFT、评测、推理和可选 RL 串成可运行、可测量、可修改的 LLM 实验闭环。

## 项目目标
仓库以“低成本”和“低认知复杂度”为双重约束：
- 用一个 8×H100 节点在约 1.5 小时内训练出超过 GPT-2 CORE 基准的模型；README 估算按约 `$3/GPU/hour` 计算，总成本约 `$48`，spot 实例可能更低。
- 不做大型、通用、配置层层嵌套的框架，而是提供一个单体、连贯、可读、容易 fork 的 strong baseline。
- 用 `--depth` 作为主要复杂度旋钮，再根据经验 scaling law 和 muP 风格外推自动确定宽度、头数、训练 token、batch size、学习率和 weight decay。

这意味着它追求的是“端到端理解和快速实验”，而不是生产级模型平台的通用性、兼容性或海量配置能力。

## 端到端流水线
`runs/speedrun.sh` 是理解仓库最重要的入口，执行顺序是：

1. 安装环境并准备数据。
2. 下载约 8 个 shard，训练 32K BPE tokenizer，并评估压缩率。
3. 后台继续下载预训练数据。
4. 用 `scripts/base_train.py` 预训练 base model。
5. 用 BPB、DCLM CORE 和样例生成评估 base model。
6. 用 SmolTalk、MMLU、GSM8K 混合数据做 SFT。
7. 用 ARC、MMLU、GSM8K、HumanEval 等任务评估 chat model。
8. 用 CLI 与模型对话。

`scripts/chat_rl.py` 提供基于 GSM8K 的简化 policy-gradient / “GRPO” 实验，但不在默认 speedrun 主链中。

## 架构分层

### 1. `runs/`：实验配方层
- `speedrun.sh`：从空机器到可对话模型的参考流程。
- `runcpu.sh`：把规模极度缩小，用 CPU 或 Apple Silicon 验证流程。
- `miniseries.sh`：按 depth 训练一组 compute-optimal 模型。
- `scaling_laws.sh`：做 scaling law 实验。

这一层回答“整场实验按什么顺序跑、各阶段用什么参数”。

### 2. `scripts/`：阶段控制器
- `tok_train.py` / `tok_eval.py`：tokenizer 训练与评估。
- `base_train.py` / `base_eval.py`：预训练与 base model 评估。
- `chat_sft.py` / `chat_eval.py`：监督微调与 chat 能力评估。
- `chat_rl.py`：数学任务上的可选强化学习。
- `chat_cli.py`：交互入口。
- `infer_bench.py`：prefill、decode、KV cache、吞吐和显存基准。

这一层回答“某一个训练或评测阶段如何调度数据、模型、优化器、checkpoint 与日志”。

### 3. `nanochat/`：可复用内核
- `gpt.py`：模型结构、初始化、forward、FLOPs/参数统计和优化器分组。
- `tokenizer.py`：Rust BPE 训练、tiktoken 推理、对话特殊 token 和 loss mask 渲染。
- `dataloader.py` / `dataset.py`：预训练数据下载、DDP 分片、BOS 对齐、best-fit packing 与恢复状态。
- `optim.py`：矩阵参数使用 Muon，embedding、lm_head 和标量参数使用 AdamW。
- `engine.py`：KV cache、prefill/decode、采样和计算器工具状态机。
- `checkpoint_manager.py`：模型与优化器状态保存/加载。
- `core_eval.py` / `loss_eval.py`：能力指标与 bits-per-byte。
- `flash_attention.py` / `fp8.py`：硬件加速路径及 fallback。

这一层回答“跨阶段复用的技术机制是什么”。

### 4. `tasks/`：任务与数据契约
每个 task 负责把原始数据转换成 conversation，并定义答案判定或 reward。`TaskMixture`、`TaskSequence` 把多个任务组合起来。

这一层同时服务训练和评测，使“能力”变成可生成样本、可打分的接口，而不是只存在于 prompt 描述中。

### 5. `tests/`：关键不变量
测试重点覆盖 tokenizer round-trip 与对话渲染、attention fallback、KV cache 推理一致性、代码执行、优化器以及 task slicing/mixture。

## 模型结构
`nanochat/gpt.py` 仍是 decoder-only Transformer，但包含较多经过实验选择的现代改造：
- RoPE，不使用可学习位置 embedding。
- RMSNorm、QK norm、无 bias Linear、ReLU² MLP。
- GQA，减少推理时 KV cache 成本。
- `SSSL` sliding-window pattern：多数层只看短窗口，周期性 full-context，最后一层强制长窗口。
- Flash Attention 3，其他环境回退到 PyTorch SDPA。
- token embedding 与 lm head 不共享权重。
- alternating value embedding、可学习 residual/x0 mixing、smear 与 backout 等实验性结构。
- logits softcap 后再计算交叉熵。

不要把所有这些特性一次性当作 Transformer 入门内容。学习时应先看清 `embedding → repeated Block(attention + MLP) → norm → lm_head → cross-entropy` 主干，再逐个研究额外改造解决什么成本或优化问题。

## 训练系统的关键设计

### 单一 depth 旋钮
`base_train.py` 令 `model_dim = depth × aspect_ratio`，再计算 head 数和 GQA 配置。模型参数量确定后，代码按 scaling law 推导：
- 目标训练 token 数
- 最优 total batch size
- batch-size learning-rate correction
- 随模型规模变化的 weight decay
- 总训练 step 数

这把大量超参数从“用户配置”变成“仓库维护者的研究结论”。优点是可比较、低门槛；代价是这些外推包含经验假设，不能视为普适定律。

### 显式精度与硬件路径
模型不依赖 `autocast`，而是用全局 `COMPUTE_DTYPE` 显式控制计算精度：master weight 保持 FP32，forward 时 Linear weight 转为 BF16/FP16 等计算 dtype；H100 可启用 FP8。CUDA、CPU/MPS 和不同 attention 实现有不同路径。

### 数据 packing 与 loss mask
- 预训练 loader 给文档加 BOS，以 best-fit 方式装入固定长度序列，并记录 shard/row-group/epoch 位置以支持恢复。
- SFT tokenizer 把 conversation 渲染成角色特殊 token，并只在 assistant completion 上计算 loss；用户 prompt、工具输出、padding 等位置用 `-1` 忽略。

### 优化器分工
大矩阵参数由 Muon 更新，embedding、unembedding、value embedding 和标量参数由 AdamW 更新。训练过程还动态调度 learning rate、Muon momentum 和 weight decay。

## 评测体系
项目至少有三类指标：
- **BPB（bits per byte）**：比 token-level loss 更少受词表大小影响，用于观察语言建模质量。
- **CORE**：DCLM 的 base model 综合能力指标；当前 speedrun 目标是超过 GPT-2 的 `0.256525`。
- **ChatCORE**：对 ARC-Easy、ARC-Challenge、MMLU、GSM8K、HumanEval 做去随机基线后的平均。

同时监控 wall-clock time、FLOPs、tokens/sec、MFU、VRAM，以及推理阶段的 TTFT、TPOT、KV cache 和带宽利用。这体现了 [[wiki/concepts/AI评估|AI评估]] 中“能力、成本和系统性能必须同时测”的原则。

## 核心启发
- **harness 比单个模型文件更接近真实研究对象。** 模型效果来自数据、tokenizer、架构、优化器、精度、评测和实验节奏的共同作用。
- **减少配置也是一种架构选择。** 单一 depth 旋钮把复杂度集中在代码和实验依据中，提升可比性，但也减少自由度。
- **先建立闭环，再做局部创新。** 能从数据跑到指标和对话，才能判断一次模型修改是否真正有价值。
- **小模型适合学习系统，不适合学习幻觉。** CPU demo 可以验证链路和代码理解，不能代表完整训练配方的能力结论。
- **仓库是研究快照。** 其中包含明确标记为假设或实验性的设计，应该用消融和指标验证，而不是把当前实现当作教科书标准答案。

## 已整合到
- [[wiki/syntheses/nanochat 架构与学习路径|nanochat 架构与学习路径]]
- [[wiki/entities/Andrej Karpathy|Andrej Karpathy]]
- [[wiki/concepts/AI评估|AI评估]]
- [[wiki/concepts/软件工程|软件工程]]

