FROM ubuntu:16.04 as builder

ARG user=indy
ENV HOME="/home/$user"
WORKDIR $HOME
RUN mkdir ./bin ./lib

# Install environment
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        automake \
        bison \
        build-essential \
        ca-certificates \
        cmake \
        curl \
        flex \
        git \
        libbz2-dev \
        libffi-dev \
        libgflags-dev \
        libgmp-dev \
        liblz4-dev \
        libncurses5-dev \
        libreadline-gplv2-dev \
        libsnappy-dev \
        libsodium-dev \
        libsqlite3-dev \
        libssl-dev \
        libtool \
        libzmq3-dev \
        pkg-config \
        zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

ARG pbc_lib_ver=0.5.14

# Build and install pbc library
RUN curl -o pbc-${pbc_lib_ver}.tar.gz https://crypto.stanford.edu/pbc/files/pbc-${pbc_lib_ver}.tar.gz && \
    tar xzvf pbc-${pbc_lib_ver}.tar.gz && \
    cd pbc-${pbc_lib_ver} && \
    ./configure && \
    make install && \
    cd .. && \
    cp /usr/local/lib/libpbc*.so "$HOME/lib" && \
    rm -rf pbc-${pbc_lib_ver}*

ARG rocksdb_lib_ver=5.13.fb

# Build and install rocksdb library
RUN git clone https://github.com/facebook/rocksdb.git && \
    cd rocksdb && \
	git checkout ${rocksdb_lib_ver} && \
    CXXFLAGS="-flto -Os -s" make install-shared && \
    cd .. && \
    cp /usr/local/lib/librocksdb.so "$HOME/lib" && \
    rm -rf rocksdb

# set to --release for smaller, optimized library
ARG indy_build_flags=

ARG indy_sdk_repo=https://github.com/bcgov/indy-sdk.git
ARG indy_sdk_rev=574ca3a881d188c3fd7400d27acbe5edc4c7f666
ARG indy_crypto_repo=https://github.com/hyperledger/indy-crypto.git
ARG indy_crypto_rev=96c79b36c5056eade5a8e3bae418f5a733cc8d8d

# Install rust toolchain and indy-sdk
RUN curl -o rustup https://sh.rustup.rs && \
    chmod +x rustup && \
    ./rustup -y && \
    git clone $indy_sdk_repo && \
    git clone $indy_crypto_repo && \
    cd indy-sdk/libindy && \
    git checkout ${indy_sdk_rev} && \
    $HOME/.cargo/bin/cargo build ${indy_build_flags} && \
    mv target/*/libindy.so "$HOME/lib" && \
    cd $HOME/indy-crypto/libindy-crypto && \
    git checkout ${indy_crypto_rev} && \
    $HOME/.cargo/bin/cargo build ${indy_build_flags} && \
    mv target/*/libindy_crypto.so "$HOME/lib" && \
    cd $HOME && \
    rm -rf .cargo .multirust .profile .rustup rustup indy-sdk indy-crypto

# 3.5.3+ required
ARG python_version=3.5.5

# Install pyenv and python to user home directory
ENV PYENV_ROOT="$HOME/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
RUN git clone https://github.com/pyenv/pyenv.git "$PYENV_ROOT" && \
    pyenv install $python_version && \
    pyenv global $python_version && \
    find "$PYENV_ROOT" -depth \
		\( \
			\( -type d -a \( -name test -o -name tests \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' +

ARG requirements=requirements-1.3.1-dev-408.txt

ADD $requirements requirements.txt

# Update pip and install indy python libraries
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# start fresh
FROM ubuntu:16.04


ARG uid=1001
ARG user=indy
ARG python_version=3.5.5

ENV HOME="/home/$user" \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHON_VERSION="$python_version" \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    RUST_LOG=warning \
    SHELL=/bin/bash

ENV SUMMARY="von-image including Python $python_version, indy-sdk, and indy-node" \
    DESCRIPTION="von-image provides a consistent base image for running VON python web \
components. Based on Ubuntu xenial, this image includes Python $python_version \
as well as indy-sdk, indy-node, and supporting Python libraries such as von-agent and didauth."

# Add indy user
RUN useradd -U -ms /bin/bash -u $uid $user

# Install environment
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        bzip2 \
        curl \
        git \
        libffi6 \
        libgflags2v5 \
        libgmp10 \
        liblz4-1 \
        libncurses5 \
        libreadline5 \
        libsnappy1v5 \
        libsodium18 \
        libzmq5 \
        openssl \
        sqlite3 \
        zlib1g && \
    rm -rf /var/lib/apt/lists/* /usr/share/doc/*

WORKDIR $HOME

# Copy build results
COPY --from=builder --chown=indy:indy $HOME .

# Add selected version of python to the path
ENV PYENV_ROOT="$HOME/.pyenv"
ENV PATH="$HOME/bin:$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
# Support standard python paths used in scripts
RUN ln -s "$PYENV_ROOT/shims/python" /usr/bin/python && \
    ln -s "$PYENV_ROOT/shims/python3" /usr/bin/python3 && \
    ln -s "$PYENV_ROOT/shims/pip" /usr/bin/pip && \
    ln -s "$PYENV_ROOT/shims/pip3" /usr/bin/pip3

# Make libraries resolvable by python
ENV LD_LIBRARY_PATH="$HOME/lib:$LD_LIBRARY_PATH"

USER $user

CMD ["bash"]
