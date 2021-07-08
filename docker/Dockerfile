FROM gh0st42/coreemu7:latest
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
    gnuplot \
    && apt-get clean

WORKDIR /root
RUN git clone https://github.com/gh0st42/core-automator &&\
    pip install appjar &&\
    cp core-automator/*.py /usr/local/bin &&\
    rm -rf core-automator

# needed for periodic-file-generator
RUN pip install lorem-text

WORKDIR /usr/local/bin
COPY scripts/* /usr/local/bin/
COPY analyzers/* /usr/local/bin/

EXPOSE 22
EXPOSE 50051

# ADD extra /extra
VOLUME /shared

WORKDIR /shared

COPY entryPoint.sh /root/entryPoint.sh
ENTRYPOINT "/root/entryPoint.sh"

