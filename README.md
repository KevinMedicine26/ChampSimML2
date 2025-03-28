# ChampSim ML 预取器使用指南

## 项目概述

ChampSim ML 预取器项目是一个用于评估内存预取器性能的框架，基于 ChampSim 模拟器。该项目允许用户将预取决策直接从文本文件导入，无需通过模型训练步骤，从而简化了预取器性能评估过程。

## 环境设置

### Docker 环境

项目使用 Docker 容器提供一个一致的运行环境，避免依赖问题。

1. 启动 Docker 容器：

```bash
docker-compose up -d
```

2. 进入容器：

```bash
docker-compose exec champsim bash
```

### 目录结构

```
champsim/
├── src/                 # 源代码目录
├── traces/              # 执行轨迹文件目录 (.champsimtrace.xz)
├── load_traces/         # 加载轨迹文件目录 (.txt.xz)
├── prefetchers/         # 预取文件目录 (.txt)
└── results/             # 模拟结果目录
```

## 基本工作流程

### 1. 构建 ChampSim 二进制文件

首次使用时，需要构建 ChampSim 二进制文件：

```bash
cd /champsim/src
python3 ml_prefetch_sim.py build
```

这将构建三个二进制文件：

- 不带预取器的基准版本
- 带有最佳偏移(Best Offset)预取器的版本
- 可从文件读取预取指令的版本

> **注意**：如果构建过程中出现错误，可能是脚本文件的行尾符号问题。使用以下命令修复：
>
> ```bash
> apt-get update && apt-get install -y dos2unix
> dos2unix build_champsim.sh
> ```

### 2. 准备轨迹文件

如果没有轨迹文件，可以使用项目提供的下载脚本获取：

```bash
cd /champsim
./src/download.sh
```

### 3. 准备预取文件

预取文件是一个文本文件，每行包含两个数字：指令 ID 和预取地址。例如：

```
3659 7f8400
3659 7f8440
5433 8001c0
```

如果需要从其他格式转换，可以使用转换工具：

```bash
python3 /champsim/src/convert_txt_to_prefetch.py 输入文件 /champsim/prefetchers/输出文件.txt [选项]
```

选项说明：

- `--format csv` - 指定输入格式为 CSV (默认为"default")
- `--delimiter ","` - CSV 分隔符 (默认为逗号)
- `--instr-col 0` - 指令 ID 在 CSV 中的列索引 (默认为 0)
- `--addr-col 1` - 地址在 CSV 中的列索引 (默认为 1)

### 4. 运行模拟

运行基准测试和预取器测试：

```bash
python3 ml_prefetch_sim.py run /champsim/traces/轨迹文件.champsimtrace.xz --prefetch /champsim/prefetchers/预取文件.txt
```

如果只想测试预取器（跳过基准测试）：

```bash
python3 ml_prefetch_sim.py run /champsim/traces/轨迹文件.champsimtrace.xz --prefetch /champsim/prefetchers/预取文件.txt --no-base
```

> **注意**：模拟可能需要较长时间运行（根据轨迹大小可能需要几分钟到几小时）。模拟器会定期输出"心跳"信息显示进度。

其他可选参数：

- `--results-dir 结果目录` - 指定结果输出目录 (默认为 `./results`)
- `--num-instructions N` - 模拟的指令数（百万条）(默认为 SPEC:500, GAP:300)
- `--name 自定义名称` - 为预取器指定一个名称 (默认为 "from_file")

### 5. 评估结果

```bash
python3 ml_prefetch_sim.py eval
```

这将生成一个 CSV 文件（默认为 `./stats.csv`），包含以下性能指标：

- 准确率(Accuracy) - 有用预取的百分比
- 覆盖率(Coverage) - 有用预取占总缺失的百分比
- MPKI(每千指令缺失数) - 越低越好
- MPKI 改进 - 相对于基准的改进百分比
- IPC(每周期指令数) - 越高越好
- IPC 改进 - 相对于基准的改进百分比

## 轨迹文件区别

项目中有两种不同类型的轨迹文件：

1. **执行轨迹文件** (`traces/` 目录，`.champsimtrace.xz` 格式)

   - 用于 ChampSim 模拟器的实际执行
   - 包含完整的程序执行信息，如指令地址、数据地址等
   - 用于评估处理器架构、缓存系统和预取策略的整体性能

2. **加载轨迹文件** (`load_traces/` 目录，`.txt.xz` 格式)
   - 记录程序内存加载(load)操作
   - 用于分析内存访问模式，生成预取策略
   - 数据格式：`指令ID, 时钟周期, 加载地址, 指令指针, LLC命中/未命中`

## 预取文件格式

预取文件格式要求：

- 每行包含两个由空格分隔的值：`<指令ID> <预取地址>`
- 每个指令 ID 最多可以有两个预取
- 预取地址应为十六进制格式(不含"0x"前缀)
- 预取必须按照轨迹中出现的顺序排列

## 实例演示

完整工作流程示例：

```bash
# 进入容器
docker-compose exec champsim bash

# 进入工作目录
cd /champsim/src

# 构建 ChampSim
python3 ml_prefetch_sim.py build

# 运行模拟
python3 ml_prefetch_sim.py run /champsim/traces/471.omnetpp-s0.trace.gz --prefetch /champsim/prefetchers/prefetch14_CF01S.txt

# 等待模拟完成（可能需要一段时间）

# 评估结果
python3 ml_prefetch_sim.py eval

# 查看结果
cat stats.csv
```

## 常见问题解决

1. **脚本执行错误**：如果遇到 `./build_champsim.sh: not found` 错误，使用 `dos2unix` 转换脚本文件：

   ```bash
   apt-get update && apt-get install -y dos2unix
   dos2unix build_champsim.sh
   ```

2. **找不到轨迹文件**：确保轨迹文件位于正确目录，可能需要先运行 `download.sh` 脚本下载。

3. **模拟运行时间长**：ChampSim 是一个周期精确的模拟器，运行需要时间，请耐心等待。可以通过 `--no-base` 选项仅运行自定义预取器节省时间。

4. **结果评估错误**：确保完整运行所有模拟，不要中途中断，否则可能导致评估结果不完整。

example 1 ：

TRACE
首选：ML-DPC/LoadTraces/spec06/471.omnetpp-s0.txt.xz
理由：
471.omnetpp 是网络仿真程序，包含复杂的内存访问模式（不规则访问）、分支逻辑和适度的计算需求。
它不像 bwaves（计算密集）或 mcf（内存密集）那样极端，适合测试通用预取器的适应性。
.txt.xz 格式表明这是提取的负载数据，可能更轻量，专注于内存访问分析。
适用性：适合需要平衡内存和计算的通用任务。

下载地址
ML-DPC/LoadTraces/spec06/471.omnetpp-s0.txt.xz
https://utexas.box.com/shared/static/8shjfyw05w0n3prerb06rohsl08dfsmf.xz
ML-DPC/ChampSimTraces/spec06/471.omnetpp-s0.trace.gz https://utexas.box.com/shared/static/1y1oq6c3q4zyf6rju2ejcc01xt5p25a6.gz

prefetch14.txt 预取器文件
