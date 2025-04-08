
ARG BASE_IMAGE=nvidia/cuda:12.8.0-cudnn-devel-ubuntu20.04
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=noetic

ARG USER_NAME=carla
ARG USER_ID=1000

# Update the package list and install prerequisites
RUN apt-get update && apt-get install -y \
    lsb-release \
    gnupg2 \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# OpenGL Nonsense
RUN apt update && apt -y install \
    sudo \
    libgl1-mesa-glx \
    mesa-utils \
    && rm -rf /var/lib/apt/lists/*

## ROS installation ##
RUN sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' && \
    curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

# Update and install ROS Noetic
RUN apt-get update && apt-get install -y \
    ros-noetic-desktop-full \
    python3-rosdep \
    python3-rosinstall \
    python3-rosinstall-generator \
    python3-wstool \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
    
RUN sudo rosdep init && rosdep update

RUN apt-get update && apt-get install python3-catkin-tools -y && \
    rm -rf /var/lib/apt/lists/*

# Basic packages
RUN apt-get -y update && apt-get -y install \
    sudo \
    python3-pip \
    curl \
    doxygen \
    wget \
    vim \
    git \
    cmake \
    git-lfs \
    build-essential \
    libegl1-mesa \
    vulkan-tools \
    nano \
    ros-noetic-depthimage-to-laserscan \
    ros-noetic-laser-scan-matcher \
    ros-noetic-rtabmap-ros \
    ros-noetic-hector-slam \
    ros-noetic-joy \
    ros-noetic-turtlebot3-gazebo \
    ros-noetic-turtlebot3-bringup \
    ros-noetic-turtlebot3-navigation \
    ros-noetic-image-view \
    ros-noetic-rqt \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get -y update \
    && apt-get -y install \
    libglew-dev \
    libassimp-dev \
    libboost-all-dev \
    libgtk-3-dev \
    libglfw3-dev \
    libavdevice-dev \
    libavcodec-dev \
    libeigen3-dev \
    libxxf86vm-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -l -u ${USER_ID} -s /bin/bash ${USER_NAME} \
    && usermod -aG video ${USER_NAME} \
    && export PATH=$PATH:/home/${USER_NAME}/.local/bin

RUN echo "${USER_NAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN echo ${USER_NAME}

# Install OpenCV 4.4.0
WORKDIR /opencv_build

# OpenCV:
# Download and extract OpenCV and OpenCV contrib
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.4.0.zip && \
    wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.4.0.zip && \
    unzip opencv.zip && \
    unzip opencv_contrib.zip && \
    rm opencv.zip opencv_contrib.zip
    
RUN cd opencv-4.4.0 && \
    mkdir build && \
    cd build && \
    cmake \
    -D CMAKE_BUILD_TYPE=Release \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv_build/opencv_contrib-4.4.0/modules \
    -D PYTHON_EXECUTABLE=/usr/bin/python3 \
    -D WITH_TBB=ON \
    -D WITH_V4L=ON \
    -D WITH_FFMPEG=ON \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_TESTS=OFF \
    -D BUILD_PERF_TESTS=OFF \
    -D BUILD_opencv_python2=OFF \
    -D BUILD_opencv_python3=ON \
    -D CMAKE_CXX_FLAGS="-std=c++14" .. && \
    make -j$(nproc)

RUN cd opencv-4.4.0/build/ && \
    make install && \
    ldconfig

WORKDIR / 

# Install Pangolin dependencies
RUN apt-get update && apt-get install -y \
    libglew-dev \
    libboost-dev libboost-thread-dev libboost-filesystem-dev \
    libxkbcommon-dev \
    wayland-protocols \
    libegl1-mesa-dev \
    libwayland-dev \
    libxrandr-dev \
    libeigen3-dev \
    libzmq3-dev \
    libpython3-dev

# Clone and build specific version of Pangolin
RUN git clone --branch v0.6 https://github.com/stevenlovegrove/Pangolin.git && \
    cd Pangolin && \
    mkdir build && \
    cd build && \
    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_CXX_FLAGS="-std=c++14" \
        -DBUILD_EXAMPLES=OFF \
        -DBUILD_TOOLS=OFF && \
    make -j$(nproc) && \
    make install && \
    cd ../.. && \
    rm -rf Pangolin

RUN apt-get update && apt-get install -y \
    ros-noetic-cv-bridge \
    python3-cv-bridge

# RUN sudo apt-get update && sudo add-apt-repository ppa:ubuntu-toolchain-r/test && \
#     sudo apt-get install gcc-11 g++-11 -y && \
#     rm -rf /var/lib/apt/lists/*

# Clean up build files
RUN sudo rm -rf /opencv_build

## ORB-SLAM
RUN git clone https://github.com/vikramanantha/orb_slam.git ORB_SLAM3

# Sophus
RUN cd ORB_SLAM3/Thirdparty/Sophus && \
    mkdir build && cd build && \
    cmake .. && \
    make -j$(nproc) && \
    sudo make install

# DBoW2
RUN cd ORB_SLAM3/Thirdparty/DBoW2 && \
    mkdir build && cd build && \
    cmake .. && \
    make -j$(nproc)
    
# ORBSLAM3
RUN cd ORB_SLAM3/ && \
    rm -r build && \
    mkdir build && cd build && \
    cmake .. && \
    make -j$(nproc)

USER ${USER_NAME}

WORKDIR /home/${USER_NAME}



USER ${USER_NAME}
WORKDIR /home/${USER_NAME}

RUN echo "source /opt/ros/noetic/setup.bash" >> /home/${USER_NAME}/.bashrc

SHELL ["/bin/bash", "-c"]

ENV USER_NAME=${USER_NAME}

COPY ./entrypoint.sh /entrypoint.sh
RUN sudo chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]