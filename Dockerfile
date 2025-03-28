FROM ubuntu:20.04

# 避免交互式提示
ENV DEBIAN_FRONTEND=noninteractive

# 安装必要的依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    python3 \
    python3-pip \
    curl \
    wget \
    xz-utils \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /champsim

# 复制项目文件
COPY . /champsim/

# 确保脚本可执行（逐个文件检查）
RUN if [ -f build_champsim.sh ]; then chmod +x build_champsim.sh; fi
RUN if [ -f run_champsim.sh ]; then chmod +x run_champsim.sh; fi
RUN if [ -f run_4core.sh ]; then chmod +x run_4core.sh; fi
RUN if [ -f download.sh ]; then chmod +x download.sh; fi
RUN if [ -f ml_prefetch_sim.py ]; then chmod +x ml_prefetch_sim.py; fi
RUN if [ -f convert_txt_to_prefetch.py ]; then chmod +x convert_txt_to_prefetch.py; fi

# 设置Python环境
RUN pip3 install numpy pandas matplotlib

# 尝试构建ChampSim二进制文件（如果失败也继续）
RUN if [ -f ml_prefetch_sim.py ]; then ./ml_prefetch_sim.py build || echo "Build failed but continuing"; fi

# 设置入口点
ENTRYPOINT ["/bin/bash"]