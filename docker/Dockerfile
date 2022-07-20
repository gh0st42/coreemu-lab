ARG ARCH=

FROM ${ARCH}rust:1.62.1 as builder
WORKDIR /root
RUN rustup component add rustfmt
RUN apt update && apt-get install build-essential cmake -y && rm -rf /var/lib/apt/lists/*
#RUN cargo install --bins --examples --root /usr/local --git https://github.com/gh0st42/coreemu-rs --branch coreemu8 --rev eda2ebd coreemu
RUN cargo install --bins --examples --root /usr/local --git https://github.com/gh0st42/coreemu-rs --rev 326a6f75 coreemu

FROM ${ARCH}gh0st42/coreemu7:1.0.0
LABEL Description="Docker image for network evaluations using core network emulator"


ENV DEBIAN_FRONTEND noninteractive

# evaluation dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    htop \
    sysstat \
    bwm-ng \
    ripgrep \
    fd-find \
    python3-pandas \
    python3-matplotlib \
    jq \
    tcpdump \
    gnuplot \
    lxterminal \
    less \
    netcat \
    unzip \
    openjdk-8-jdk-headless \
    tigervnc-viewer \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/* /usr/local/bin/

WORKDIR /root
RUN git clone https://github.com/gh0st42/core-automator &&\
    pip install appjar &&\
    cp core-automator/*.py /usr/local/bin &&\
    rm -rf core-automator

# needed for periodic-file-generator
RUN pip install lorem-text

WORKDIR /root
RUN wget https://sys.cs.uos.de/bonnmotion/src/bonnmotion-3.0.1.zip && \
    unzip bonnmotion* && \
    cd bonnmotion-3.0.1 && \
    ./install && \
    cp bin/bm /usr/local/bin

WORKDIR /usr/local/bin
COPY scripts/* /usr/local/bin/
COPY analyzers/* /usr/local/bin/

WORKDIR /root
RUN mkdir -p /root/.coregui/icons/ && \
    mkdir -p /root/.core
COPY coreemu-addons/icons/uav*.png /root/.coregui/icons/
COPY coreemu-addons/config.yaml /root/.coregui/
COPY coreemu-addons/nodes.conf /root/.core/

EXPOSE 22
EXPOSE 50051

# ADD extra /extra
VOLUME /shared

WORKDIR /shared

COPY entryPoint.sh /root/entryPoint.sh
ENTRYPOINT "/root/entryPoint.sh"

