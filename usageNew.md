现在用户可以通过以下方式使用这个系统:
使用默认格式的预取器文件:
./ml_prefetch_sim.py run trace.champsimtrace.xz --prefetch prefetcher.txt


使用 CSV 格式的预取器文件:
./ml_prefetch_sim.py run trace.champsimtrace.xz --prefetch prefetcher.txt


只运行自定义预取器而不运行基准测试:
./ml_prefetch_sim.py run trace.champsimtrace.xz --prefetch prefetcher.csv --format csv --delimiter "," --instr-col 0 --addr-col 1

指定结果目录和预取器名称:
./ml_prefetch_sim.py run trace.champsimtrace.xz --prefetch prefetcher.txt --no-base