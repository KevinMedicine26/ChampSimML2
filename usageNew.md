现在用户可以通过以下方式使用这个系统:
使用默认格式的预取器文件:
./ml_prefetch_sim.py run trace.champsimtrace.xz --prefetch prefetcher.txt

使用 CSV 格式的预取器文件:
./ml_prefetch_sim.py run trace.champsimtrace.xz --prefetch prefetcher.txt

只运行自定义预取器而不运行基准测试:
./ml_prefetch_sim.py run trace.champsimtrace.xz --prefetch prefetcher.csv --format csv --delimiter "," --instr-col 0 --addr-col 1

指定结果目录和预取器名称:
./ml_prefetch_sim.py run trace.champsimtrace.xz --prefetch prefetcher.txt --no-base

# ChampSim Prefetch File Format Guide

## Background

The ChampSim simulator uses a specific format for prefetch files to evaluate prefetching performance. This guide explains the format and how to create valid prefetch files from your own data.

## Prefetch File Format

Each line in a prefetch file consists of two space-separated values:

```
<unique_instruction_id> <prefetch_address>
```

Where:

- `<unique_instruction_id>`: An integer ID for the instruction that triggers the prefetch
- `<prefetch_address>`: The memory address to prefetch (in hexadecimal without the "0x" prefix)

### Example:

```
3659 7f8400
3659 7f8440
5433 8001c0
```

This example shows:

- Instruction ID 3659 generates two prefetches for addresses 0x7f8400 and 0x7f8440
- Instruction ID 5433 generates one prefetch for address 0x8001c0

## Rules and Limitations

1. Up to **two prefetches** are allowed per unique instruction ID
2. If more than two prefetches are provided for an instruction ID, only the first two will be used
3. Prefetches must be in the same order as they appear in the trace
4. The instruction ID must match exactly the ID from the corresponding load trace

## Creating a Custom Prefetch File

You can create a prefetch file manually or use the provided `convert_txt_to_prefetch.py` script to convert from various formats.

### Using the Conversion Script

```bash
python convert_txt_to_prefetch.py input.txt output.prefetch --format csv --delimiter "," --instr-col 0 --addr-col 1
```

## Running With Your Prefetch File

After creating your prefetch file, you can evaluate its performance with ChampSim:

```bash
./ml_prefetch_sim.py run trace.champsimtrace.xz --prefetch my_prefetches.txt
```

This will run ChampSim using your prefetch file and generate results in the results directory.
