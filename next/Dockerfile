FROM rust:1.45-slim-buster as builder

ARG user=indy
ENV HOME="/home/$user"
WORKDIR $HOME
RUN mkdir -p .local/bin .local/etc .local/lib

# Install environment
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    automake \
    build-essential \
    ca-certificates \
    cmake \
    curl \
    git \
    libbz2-dev \
    libffi-dev \
    libgmp-dev \
    liblzma-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libsecp256k1-dev \
    libsodium-dev \
    libsqlite3-dev \
    libssl-dev \
    libtool \
    libzmq3-dev \
    pkg-config \
    python3 \
    python3-pip \
    python3-setuptools \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

# set to --release for smaller, optimized library
ARG indy_build_flags=--release

# overridden by the build script
ARG indy_sdk_url=https://codeload.github.com/bcgov/indy-sdk/tar.gz/574ca3a881d188c3fd7400d27acbe5edc4c7f666

# make local libs and binaries accessible
ENV PATH="$HOME/.local/bin:$PATH"
ENV LIBRARY_PATH="$HOME/.local/lib:$LIBRARY_PATH"
RUN ln -s `which pip3` "$HOME/.local/bin/pip" && \
    ln -s `which python3` "$HOME/.local/bin/python"

# Download and extract indy-sdk
RUN mkdir indy-sdk && \
    curl "${indy_sdk_url}" | tar -xz -C indy-sdk

# Build and install indy-sdk
WORKDIR $HOME/indy-sdk
RUN cd indy-sdk*/libindy && \
    cargo build ${indy_build_flags} && \
    cp target/*/libindy.so "$HOME/.local/lib" && \
    cargo clean

# Package and install python3-indy
RUN tar czvf python3-indy.tgz -C indy-sdk*/wrappers/python . && \
    pip install --no-cache-dir --user python3-indy.tgz && \
    rm python3-indy.tgz

# Build and install indy-cli
RUN cd indy-sdk*/cli && \
    cargo build ${indy_build_flags} && \
    cp target/*/indy-cli "$HOME/.local/bin" && \
    cargo clean

# Build and install postgres_storage plugin
RUN cd indy-sdk*/experimental/plugins/postgres_storage && \
    cargo build ${indy_build_flags} && \
    cp target/*/libindystrgpostgres.so "$HOME/.local/lib" && \
    cargo clean

# Clean up SDK
WORKDIR $HOME
RUN rm -rf indy-sdk


ARG indy_vdr_url=https://codeload.github.com/andrewwhitehead/indy-vdr/tar.gz/8b2c34fd8012a92ad1d22ff277d8b5352f4394bb

# Download and extract indy-vdr
RUN mkdir indy-vdr && \
    curl "${indy_vdr_url}" | tar -xz -C indy-vdr

# Build and install indy-vdr
# Ensure libindy_vdr.so is included in the python package to avoid 'Library not loaded from python package' messages.
WORKDIR $HOME/indy-vdr
RUN cd indy-vdr* && \
    cargo build ${indy_build_flags} && \
    cp target/*/libindy_vdr.so "$HOME/.local/lib" && \
    cp target/*/libindy_vdr.so wrappers/python/indy_vdr && \
    cp target/*/indy-vdr-proxy "$HOME/.local/bin" && \
    cargo clean

# Package and install indy_vdr python wrapper
RUN tar czvf indy_vdr.tgz -C indy-vdr*/wrappers/python . && \
    pip install --no-cache-dir --user indy_vdr.tgz && \
    rm indy_vdr.tgz

# Clean up VDR
WORKDIR $HOME
RUN rm -rf indy-vdr


ARG indy_shared_url=https://codeload.github.com/bcgov/indy-shared-rs/tar.gz/e407a7ddbe38fa2de779ae69f6159afbd699b2e2

# Download and extract indy-credx
RUN mkdir indy-shared-rs && \
    curl "${indy_shared_url}" | tar -xz -C indy-shared-rs

# Build and install indy-credx
WORKDIR $HOME/indy-shared-rs
RUN cd indy-shared-rs* && \
    cargo build -p indy-credx ${indy_build_flags} && \
    cp target/*/libindy_credx.so "$HOME/.local/lib" && \
    cp target/*/libindy_credx.so wrappers/python/indy_credx && \
    cargo clean

# Package and install indy_credx python wrapper
RUN tar czvf indy_credx.tgz -C indy-shared-rs*/wrappers/python . && \
    pip install --no-cache-dir --user indy_credx.tgz && \
    rm indy_credx.tgz

# Clean up indy-credx
WORKDIR $HOME
RUN rm -rf indy-shared-rs


ARG aries_askar_url=https://codeload.github.com/andrewwhitehead/aries-askar/tar.gz/57a631bfcf8b71560edcef8fc901e4ce0ace60df

# Download and extract aries-askar
RUN mkdir aries-askar && \
    curl "${aries_askar_url}" | tar -xz -C aries-askar

# Build and install aries-askar
WORKDIR $HOME/aries-askar
RUN cd aries-askar* && \
    cargo build ${indy_build_flags} && \
    cp target/*/libaries_askar.so "$HOME/.local/lib" && \
    cp target/*/libaries_askar.so wrappers/python/aries_askar && \
    cargo clean

# Package and install aries_askar python wrapper
RUN tar czvf aries_askar.tgz -C aries-askar*/wrappers/python . && \
    pip install --no-cache-dir --user aries_askar.tgz && \
    rm aries_askar.tgz

# Clean up aries-askar
WORKDIR $HOME
RUN rm -rf aries-askar



# Install indy python libraries and other dependencies
ADD requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt && rm requirements.txt


## Start fresh (new image) ##
FROM debian:buster-slim


ARG uid=1001
ARG user=indy
ARG python_version=3.7.4
ARG tag_name=von-image
ARG tag_version=

ENV HOME="/home/$user" \
    APP_ROOT="$HOME" \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PIP_NO_CACHE_DIR=off \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    RUST_LOG=warning \
    SHELL=/bin/bash \
    SUMMARY="von-image including Python version and indy-sdk" \
    DESCRIPTION="von-image provides a consistent base image for running VON python \
    web components. Based on Debian Buster, this image includes indy-sdk \
    and supporting libraries."

LABEL summary="$SUMMARY" \
    description="$DESCRIPTION" \
    io.k8s.description="$DESCRIPTION" \
    io.k8s.display-name="von-image $tag_version" \
    name="$tag_name" \
    version="$tag_version" \
    maintainer=""

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
    less \
    libffi6 \
    libgmp10 \
    liblzma5 \
    libncurses5 \
    libncursesw5 \
    libsecp256k1-0 \
    libzmq5 \
    net-tools \
    openssl \
    python3 \
    python3-pip \
    python3-setuptools \
    sqlite3 \
    vim-tiny \
    zlib1g && \
    rm -rf /var/lib/apt/lists/* /usr/share/doc/*

WORKDIR $HOME

# Copy build results
COPY --from=builder --chown=indy:indy $HOME .

COPY --chown=indy:indy bin/ $HOME/.local/bin/
RUN chmod ug+rwx $HOME/.local/bin/*

# Add local binaries and aliases to path
ENV PATH="$HOME/.local/bin:$PATH"

# Make libraries resolvable by python
ENV LD_LIBRARY_PATH="$HOME/.local/lib:$LD_LIBRARY_PATH"
RUN echo "$HOME/.local/lib" > /etc/ld.so.conf.d/local.conf && ldconfig

# - In order to drop the root user, we have to make some directories writable
#   to the root group as OpenShift default security model is to run the container
#   under random UID.
RUN usermod -a -G 0 indy

# Create standard directories to allow volume mounting and set permissions
# Note: PIP_NO_CACHE_DIR environment variable should be cleared to allow caching
RUN mkdir -p \
    $HOME/.aries_cloudagent \
    $HOME/.cache/pip/http \
    $HOME/.indy-cli/networks \
    $HOME/.indy_client/wallet \
    $HOME/.indy_client/pool \
    $HOME/.indy_client/ledger-cache \
    $HOME/ledger/sandbox/data \
    $HOME/log

# The root group needs access the directories under $HOME/.indy_client for the container to function in OpenShift.
# Also ensure the permissions on the python 'site-packages' folder are set correctly.
RUN chown -R indy:root $HOME/.indy_client \
    && chmod -R ug+rw $HOME/log $HOME/ledger $HOME/.aries_cloudagent $HOME/.cache $HOME/.indy-cli $HOME/.indy_client \
    && chmod +rx $(python -m site --user-site)

USER $user

CMD ["bash"]
