# ChampSim ML Prefetcher 用法指南

## 项目概述

本项目用于评估预取器(prefetcher)对计算机内存系统性能的影响。通过 ChampSim 模拟器，可以测试不同预取策略的效果，包括准确率、覆盖率和 IPC(每周期指令数)改进等指标。

## 环境设置

### 目录结构

```
ChampSimML2/
├── src/                 # 源代码文件
├── traces/              # ChampSim执行轨迹文件(.champsimtrace.xz)
├── load_traces/         # 加载轨迹文件(.txt/.txt.xz)
├── prefetchers/         # 预取文件(.txt)
└── results/             # 模拟结果
```

### Docker 环境

1. 启动 Docker 容器：

```bash
docker-compose up -d
```

2. 进入容器：

```bash
docker-compose exec champsim bash
```

## 基本工作流程

### 1. 构建 ChampSim 二进制文件

```bash
cd /champsim/src

python3 ml_prefetch_sim.py build
```

这将构建三个二进制文件：

- 无预取器基准版本
- 最佳偏移(Best Offset)预取器版本
- 从文件读取预取指令的版本

### 2. 准备预取文件

如果你已有预取文件，可以直接使用。如果需要从其他格式转换，可以使用转换工具：

```bash
python3 convert_txt_to_prefetch.py /champsim/load_traces/your_file.txt /champsim/prefetchers/output.txt [选项]
```

选项说明：

- `--format csv` - 指定输入格式为 CSV (默认为"default")
- `--delimiter ","` - CSV 分隔符 (默认为逗号)
- `--instr-col 0` - 指令 ID 在 CSV 中的列索引 (默认为 0)
- `--addr-col 1` - 地址在 CSV 中的列索引 (默认为 1)

### 3. 运行模拟

```bash
python3 ml_prefetch_sim.py run /champsim/traces/trace.champsimtrace.xz --prefetch /champsim/prefetchers/output.txt
```

这会同时运行基准测试和你的预取器。如果只想测试你的预取器：

```bash
python3 ml_prefetch_sim.py run /champsim/traces/trace.champsimtrace.xz --prefetch /champsim/prefetchers/output.txt --no-base
```

其他选项：

- `--results-dir /path/to/results` - 指定结果目录 (默认为`./results`)
- `--num-instructions N` - 模拟的指令数 (百万条) (默认为 SPEC:500, GAP:300)
- `--name custom_name` - 为预取器指定一个名称 (默认为"from_file")

### 4. 评估结果

```bash
python3 ml_prefetch_sim.py eval
```

这将生成一个 CSV 文件(默认为`./stats.csv`)，包含以下指标：

- 准确率(Accuracy) - 有用预取的百分比
- 覆盖率(Coverage) - 有用预取占总缺失的百分比
- MPKI(每千指令缺失数) - 越低越好
- MPKI 改进 - 相对于基准的改进百分比
- IPC(每周期指令数) - 越高越好
- IPC 改进 - 相对于基准的改进百分比

选项说明：

- `--results-dir /path/to/results` - 指定结果目录
- `--output-file /path/to/output.csv` - 指定输出文件

## 预取文件格式

预取文件每行包含两个由空格分隔的值：

```
<指令ID> <预取地址>
```

例如：

```
3659 7f8400
3659 7f8440
5433 8001c0
```

规则：

- 每个指令 ID 最多可以有两个预取
- 预取地址应为十六进制格式(不含"0x"前缀)
- 预取必须按照轨迹中出现的顺序排列

## 常见问题

1. **无法找到轨迹文件**：确保轨迹文件放在正确的目录(`/champsim/traces/`)中

2. **构建失败**：检查是否有所有必要的依赖，尝试手动运行`./build_champsim.sh`查看详细错误

3. **预取文件格式错误**：确保预取文件格式正确，使用`convert_txt_to_prefetch.py`进行转换

4. **Docker 卷挂载问题**：确保在 docker-compose.yml 中正确设置了卷挂载

## 示例命令

完整工作流程示例：

```bash
# 构建
cd /champsim/src
python3 ml_prefetch_sim.py build

# 转换预取文件
python3 convert_txt_to_prefetch.py /champsim/load_traces/input.txt /champsim/prefetchers/prefetch.txt

# 运行模拟
python3 ml_prefetch_sim.py run /champsim/traces/429.mcf-s0.trace.xz --prefetch /champsim/prefetchers/prefetch.txt

# 评估结果
python3 ml_prefetch_sim.py eval
```

## 高级用法

- 测试多种预取策略：准备多个预取文件并逐一测试
- 批量处理：编写脚本自动处理多个轨迹文件
- 结果分析：使用 Python 脚本进一步分析 stats.csv 文件

troubleshooting

├── traces/ # ChampSim 执行轨迹文件(.champsimtrace.xz)
├── load_traces/ # 加载轨迹文件(.txt/.txt.xz)
这两种轨迹文件在 ChampSim 项目中有明显的区别：

## ChampSim 执行轨迹文件 (Execution Traces)

存放在 `traces/` 目录中，格式为 `.champsimtrace.xz`

**用途**：

- 这些是 ChampSim 模拟器的输入文件，用于模拟 CPU 执行指令的完整过程
- 包含指令地址、数据地址、指令类型等完整的程序执行信息
- 用于评估处理器架构、缓存系统和预取策略的整体性能

**特点**：

- 通常使用 xz 格式压缩（文件名以.xz 结尾）
- 格式为二进制，不能直接阅读
- 这些文件包含了完整的程序执行轨迹，用于计算 IPC 等性能指标

## 加载轨迹文件 (Load Traces)

存放在 `load_traces/` 目录中，格式为 `.txt` 或 `.txt.xz`

**用途**：

- 这些文件记录了程序中的内存加载(load)操作
- 主要用于分析内存访问模式，生成预取策略
- 是生成预取文件的基础数据

**特点**：

- 以文本格式存储，可以直接阅读
- 每行通常包含: 指令 ID, 时钟周期, 加载地址, 指令指针, LLC 命中/未命中标记
- 格式例如: `3659, 12345, 0x7f8400, 0x400a23, 1`

## 关系与工作流程

1. **数据流向**：

   - 加载轨迹文件(Load Traces) → 分析内存访问模式 → 生成预取文件
   - 执行轨迹文件(Execution Traces) + 预取文件 → ChampSim 模拟执行 → 性能结果

2. **核心区别**：
   - 加载轨迹文件只包含内存加载操作，用于分析和生成预取策略
   - 执行轨迹文件包含完整的程序执行信息，用于全面评估系统性能

简单来说，加载轨迹用于"学习"内存访问模式并生成预取策略，而执行轨迹则用于评估这些预取策略对整体系统性能的影响。

471.omnetpp-s0.trace.gz - 这是执行轨迹文件，应放在 traces/ 目录中

注意：文件扩展名是.gz 而不是.xz，ChampSim 通常使用.xz 格式，但应该也能处理.gz 格式

471.omnetpp-s0.txt.xz - 这是加载轨迹文件，应放在 load_traces/ 目录中
prefetch14.txt - 这似乎是一个预取文件，应放在 prefetchers/ 目录中


prefetch14_CF01S.txt

471.omnetpp-s0.trace.gz
compile之后:
python3 ml_prefetch_sim.py run /champsim/traces/471.omnetpp-s0.trace.gz --prefetch /champsim/prefetchers/prefetch14_CF01S.txt