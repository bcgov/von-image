FROM ubuntu:16.04 as indy-builder

ARG indy_build_flags=

# Install environment
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        cmake \
        curl \
        git \
        libssl-dev \
        libsqlite3-dev \
        libsodium-dev \
        libzmq3-dev \
        pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Install rust toolchain and indy-sdk
RUN curl -o rustup https://sh.rustup.rs && \
    chmod +x rustup && \
    ./rustup -y && \
    git clone https://github.com/bcgov/indy-sdk.git && \
    cd indy-sdk/libindy && \
    $HOME/.cargo/bin/cargo build ${indy_build_flags} && \
    mv target/*/libindy.so /usr/lib && \
    cd $HOME && \
    rm -rf .cargo .rustup indy-sdk


# start fresh
FROM ubuntu:16.04


ARG uid=1001
ARG indy_stream=master

ARG indy_anoncreds_ver=1.0.32
ARG indy_crypto_ver=0.2.0
ARG indy_node_ver=1.2.297
ARG indy_plenum_ver=1.2.237
ARG python3_indy_ver=1.3.1-dev-408

ENV HOME=/home/indy
ENV BUILD=$HOME/build

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ENV SHELL=/bin/bash

ENV RUST_LOG=warning

RUN useradd -U -ms /bin/bash -u $uid indy

# Install environment
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 68DB5E88 && \
    echo "deb https://repo.sovrin.org/deb xenial $indy_stream" >> /etc/apt/sources.list && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3.5 \
        python3-pip \
        python3-setuptools \
        python3-nacl \
        python3-psutil \
        bzip2 \
        curl \
        git \
        libzmq5 \
        openssl \
        sqlite3 \
        indy-plenum=${indy_plenum_ver} \
        indy-node=${indy_node_ver} \
        libindy-crypto=${indy_crypto_ver} \
        python3-indy-crypto=${indy_crypto_ver} && \
    rm -rf /var/lib/apt/lists/* /usr/share/doc/*

COPY --from=indy-builder /usr/lib/libindy.so /usr/lib/

# - Create a Python virtual environment for use by any application to avoid
#   potential conflicts with Python packages preinstalled in the main Python
#   installation.
# - In order to drop the root user, we have to make some directories world
#   writable as OpenShift default security model is to run the container
#   under random UID.
RUN pip3 --no-cache-dir install --upgrade pip && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip && \
    pip --no-cache-dir install virtualenv && \
    virtualenv $HOME && \
    echo "/usr/local/lib/python3.5/dist-packages/" >> $HOME/lib/python3.5/site-packages/local.pth && \
    echo "/usr/lib/python3/dist-packages/" >> $HOME/lib/python3.5/site-packages/local.pth
ENV PATH "$HOME/bin:$PATH"

RUN pip install --no-cache-dir \
        python3-indy==${python3_indy_ver} \
        "git+https://github.com/bcgov/von_agent#egg=von-agent"

WORKDIR $HOME

CMD ["bash"]
