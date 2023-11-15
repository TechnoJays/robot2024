# Based off of the wpilib suite
# https://github.com/wpilibsuite/docker-images/blob/main/ubuntu-base/Dockerfile.20.04
FROM ubuntu:20.04

RUN apt-get update && apt-get install -y apt-transport-https \
    ca-certificates \
    gnupg \
    software-properties-common \
    wget && \
    wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null && \
    apt-add-repository 'deb https://apt.kitware.com/ubuntu/ focal main' && \
    add-apt-repository ppa:git-core/ppa && \
    apt-get update && apt-get install -y tzdata && apt-get install -y \
    build-essential \
    ca-certificates \
    clang-format-10 \
    cmake \
    curl \
    fakeroot \
    g++-8 --no-install-recommends \
    gcc-8 \
    gdb \
    git \
    java-common \
    libc6-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libisl-dev \
    libopencv-dev \
    libvulkan-dev \
    libx11-dev \
    libxcursor-dev \
    libxi-dev \
    libxinerama-dev \
    libxrandr-dev \
    make \
    mesa-common-dev \
    openjdk-11-jdk \
    python-all-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    sudo \
    unzip \
    wget \
    zip \
  && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 800 --slave /usr/bin/g++ g++ /usr/bin/g++-8
RUN echo 'deb http://download.opensuse.org/repositories/home:/auscompgeek:/robotpy/xUbuntu_20.04/ /' | sudo tee /etc/apt/sources.list.d/home:auscompgeek:robotpy.list
RUN curl -fsSL https://download.opensuse.org/repositories/home:auscompgeek:robotpy/xUbuntu_20.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_auscompgeek_robotpy.gpg > /dev/null
RUN sudo apt-get update
RUN sudo apt-get install -y python3-cscore
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64

WORKDIR /