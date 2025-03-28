# ChampSim ML Prefetcher 项目结构

## 目录结构

```
champsim/
├── src/                 # 源代码目录
│   ├── ml_prefetch_sim.py    # 主要的模拟脚本
│   ├── convert_txt_to_prefetch.py  # 轨迹文件转换工具
│   ├── build_champsim.sh     # ChampSim构建脚本
│   ├── get_stats.py         # 统计数据处理脚本
│   ├── model.py            # 模型定义文件
│   ├── run_4core.sh        # 4核心模拟运行脚本
│   ├── run_champsim.sh     # ChampSim运行脚本
│   │
│   ├── src/               # ChampSim核心源代码
│   ├── inc/               # 头文件目录
│   ├── branch/            # 分支预测器实现
│   ├── prefetcher/        # 预取器实现
│   ├── replacement/       # 缓存替换策略
│   ├── tracer/           # 轨迹生成工具
│   ├── cvp_tracer/       # CVP轨迹生成工具
│   └── scripts/          # 辅助脚本
│
├── traces/             # 执行轨迹文件目录
│   └── *.champsimtrace.xz    # ChampSim执行轨迹文件
│
├── load_traces/        # 加载轨迹文件目录
│   └── *.txt.xz        # 内存加载轨迹文件
│
├── prefetchers/        # 预取文件目录
│   └── *.txt          # 预取策略文件
│
├── results/           # 模拟结果目录
│   └── stats.csv      # 性能评估结果
│
├── Dockerfile         # Docker容器配置
├── docker-compose.yml # Docker编排配置
└── usage.md          # 使用说明文档
```

## 文件说明

### 核心文件

1. **src/ml_prefetch_sim.py**
   - 主要的模拟控制脚本
   - 提供构建、运行和评估功能
   - 支持命令行参数配置

2. **src/convert_txt_to_prefetch.py**
   - 将加载轨迹转换为预取文件
   - 支持多种输入格式（CSV、默认格式等）
   - 提供格式转换选项

3. **src/build_champsim.sh**
   - ChampSim模拟器的构建脚本
   - 支持不同预取器配置的构建

4. **src/get_stats.py**
   - 处理和分析模拟统计数据
   - 生成性能报告

5. **src/model.py**
   - 定义预取模型
   - 包含模型相关的工具函数

6. **src/run_4core.sh**
   - 多核心模拟配置脚本
   - 支持4核心并行模拟

7. **src/run_champsim.sh**
   - ChampSim运行脚本
   - 提供基本的运行配置

### 数据文件

1. **traces/** 目录
   - 存放ChampSim执行轨迹文件
   - 格式：`.champsimtrace.xz`
   - 用途：完整的程序执行信息

2. **load_traces/** 目录
   - 存放内存加载轨迹文件
   - 格式：`.txt.xz`
   - 用途：分析内存访问模式

3. **prefetchers/** 目录
   - 存放预取策略文件
   - 格式：`.txt`
   - 每行格式：`<指令ID> <预取地址>`

4. **results/** 目录
   - 存放模拟结果
   - 包含性能指标（准确率、覆盖率、MPKI、IPC等）

### 配置文件

1. **Dockerfile**
   - 定义Docker容器环境
   - 包含必要的依赖和工具

2. **docker-compose.yml**
   - Docker服务编排配置
   - 定义卷挂载和容器设置

3. **usage.md**
   - 详细的使用说明文档
   - 包含工作流程和常见问题解答

### ChampSim核心组件

1. **src/src/**
   - ChampSim模拟器的核心实现
   - 包含处理器、缓存、内存系统等模块

2. **src/inc/**
   - 头文件目录
   - 定义核心数据结构和接口

3. **src/branch/**
   - 分支预测器实现
   - 包含不同分支预测算法

4. **src/prefetcher/**
   - 预取器实现目录
   - 包含各种预取策略

5. **src/replacement/**
   - 缓存替换策略实现
   - 包含LRU等替换算法

6. **src/tracer/** 和 **src/cvp_tracer/**
   - 轨迹生成工具
   - 用于生成执行轨迹和CVP轨迹

### 辅助脚本

1. **src/get_stats.py**
   - 处理和分析模拟统计数据
   - 生成性能报告

2. **src/model.py**
   - 定义预取模型
   - 包含模型相关的工具函数

3. **src/run_4core.sh**
   - 多核心模拟配置脚本
   - 支持4核心并行模拟

4. **src/run_champsim.sh**
   - ChampSim运行脚本
   - 提供基本的运行配置

## 工作流程

1. **环境准备**
   - 使用Docker容器
   - 构建ChampSim模拟器

2. **数据准备**
   - 准备执行轨迹文件
   - 准备加载轨迹文件
   - 生成预取文件

3. **运行模拟**
   - 执行基准测试
   - 执行预取器测试
   - 收集性能数据

4. **结果分析**
   - 生成性能报告
   - 分析预取器效果

## 注意事项

1. 确保所有轨迹文件放在正确的目录中
2. 预取文件格式必须符合规范
3. 使用Docker容器时注意卷挂载配置
4. 定期清理results目录以节省空间 