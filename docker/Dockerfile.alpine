FROM alpine:3.7 as builder

RUN echo '@alpine36 http://dl-cdn.alpinelinux.org/alpine/v3.6/main' >> /etc/apk/repositories

ENV HOME=/home/indy
ENV BUILD=$HOME/build
WORKDIR $BUILD

# install system packages
# need slightly older version of libsodium (before aes128 support was removed)
RUN apk update && \
    apk add --no-cache \
        bison \
        cargo \
        build-base \
        ca-certificates \
        cmake \
        flex \
        git \
        gmp-dev \
        libressl-dev@alpine36 \
        libsodium-dev@alpine36 \
        linux-headers \
        musl=1.1.18-r3 \
        python3-dev \
        rust \
        sqlite-dev \
        wget

# build pbc library (not in alpine repo)
ARG pbc_lib_ver=0.5.14
RUN wget https://crypto.stanford.edu/pbc/files/pbc-${pbc_lib_ver}.tar.gz && \
    tar xzvf pbc-${pbc_lib_ver}.tar.gz && \
    cd pbc-${pbc_lib_ver} && \
    ./configure && \
    make install && \
    cd $BUILD && \
    rm -rf pbc-${pbc_lib_ver}*

#ARG indy_build_flags=--release
ARG indy_build_flags=

# build indy-sdk from git repo
ARG indy_sdk_rev=778a38d92234080bb77c6dd469a8ff298d9b7154
RUN git clone https://github.com/hyperledger/indy-sdk.git && \
    cd indy-sdk/libindy && \
    git checkout ${indy_sdk_rev} && \
	echo Checking out prerelease version of rusqlcipher for libressl support.. && \
	git clone https://github.com/mikelodder7/rusqlcipher.git && \
    cd rusqlcipher && \
    git checkout f04967cecd299309b213f98cd9f9c5e0cf18e950 && \
    cd .. && \
    sed -i 's/^rusqlcipher =.*$/rusqlcipher = { path = "rusqlcipher", features = ["bundled"] }/' \
        Cargo.toml && \
	cargo build ${indy_build_flags} && \
    mv target/*/libindy.so /usr/local/lib && \
    cd $BUILD && \
    rm -rf indy-sdk $HOME/.cargo

# - Create a Python virtual environment for use by any application to avoid
#   potential conflicts with Python packages preinstalled in the main Python
#   installation.
# - In order to drop the root user, we have to make some directories world
#   writable as OpenShift default security model is to run the container
#   under random UID.
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip && \
    pip --no-cache-dir install virtualenv && \
    virtualenv $HOME
ENV PATH "$HOME/bin:$PATH"

ARG indy_anoncreds_ver=1.0.32
ARG indy_crypto_ver=0.2.0
ARG indy_node_ver=1.2.297
ARG indy_plenum_ver=1.2.237
ARG python3_indy_ver=1.3.1-dev-408

# install indy python packages
RUN apk add --no-cache build-base linux-headers libffi-dev autoconf automake libtool && \
	pip --no-cache-dir install \
        python3-indy==${python3_indy_ver} \
        indy-plenum-dev==${indy_plenum_ver} \
        indy-anoncreds-dev==${indy_anoncreds_ver} \
        indy-node-dev==${indy_node_ver} \
        indy-crypto==${indy_crypto_ver} \
        "git+https://github.com/bcgov/von_agent#egg=von-agent" \
        "git+https://github.com/cywolf/didauth.git" && \
    apk del build-base linux-headers libffi-dev autoconf automake libtool


# start fresh without build dependencies
FROM alpine:3.7

ARG uid=1001
ARG gid=1001

ENV HOME=/home/indy
ENV BUILD=$HOME/build

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ENV SHELL=/bin/bash

ENV RUST_LOG=warning

RUN addgroup -g $gid indy && adduser -u $uid -D -G root -G indy indy

RUN echo '@alpine36 http://dl-cdn.alpinelinux.org/alpine/v3.6/main' >> /etc/apk/repositories

WORKDIR $HOME

# install system packages
# need slightly older version of libsodium (before aes128 support was removed)
RUN apk update && \
    apk add --no-cache \
        bash \
        ca-certificates \
        git \
        gmp \
        libffi \
        libressl@alpine36 \
        libsodium@alpine36 \
        libstdc++ \
        musl=1.1.18-r3 \
        py3-pynacl \
        python3-dev \
        sqlite \
        wget

COPY --from=builder /usr/local/lib/libpbc*.so /usr/local/lib/

COPY --from=builder /usr/local/lib/libindy*.so /usr/local/lib/

COPY --from=builder $HOME $HOME

ENV PATH "$HOME/bin:$PATH"

# drop privileges
RUN chown -R indy:indy $HOME
USER indy

WORKDIR $HOME

CMD ["bash"]
