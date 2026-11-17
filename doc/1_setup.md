# Host Environment Setup

## 1. Bashrc Configuration [~/.bashrc]
```
export ROS_DOMAIN_ID=73                         #use any number
export ROS_DISTRO=jazzy                         #tested {jazzy, humble}
export CPU_ARCH=x86-64                          #tested {x86-64, arm64}
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

export MOVENSYS_ROS_VERSION=isaac-ros_4.1       #tested {general, isaac-ros_4.1, isaac-ros_3.2}
export NAVIGATION_MODEL=diffbot                 #tested {diffbot}

source ~/workspaces/movensys_ws/src/movensys-navigation/docker/nros.bash
```
```
xhost +local:docker
source ~/.bashrc
```

## 2. Set CycloneDDS buffer
```
sudo tee /etc/sysctl.d/99-network-buffers.conf << 'EOF'
net.core.rmem_max=67108864
net.core.rmem_default=67108864
net.core.wmem_max=67108864
net.core.wmem_default=67108864
EOF

sudo sysctl -p /etc/sysctl.d/99-network-buffers.conf
sysctl net.core.rmem_max net.core.rmem_default net.core.wmem_max net.core.wmem_default
```

## 3. Clone Repository
```
mkdir -p  ~/workspaces/movensys_ws/src
cd ~/workspaces/movensys_ws/src
git clone git@github.com:movensys/movensys-navigation.git
```