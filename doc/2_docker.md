# 1. Note For Isaac-ROS only
please follow this isaac-ros setup first: 
        https://nvidia-isaac-ros.github.io/v/release-3.2/getting_started/index.html
        https://nvidia-isaac-ros.github.io/v/release-4.1/getting_started/index.html
 
# 2. Docker setup
```
cd ~/workspaces/movensys_ws/src/movensys-navigation/docker
docker compose -f ${MOVENSYS_ROS_VERSION}.yaml -f movensys_navigation.${CPU_ARCH}.yaml down
docker compose -f ${MOVENSYS_ROS_VERSION}.yaml -f movensys_navigation.${CPU_ARCH}.yaml build
docker compose -f ${MOVENSYS_ROS_VERSION}.yaml -f movensys_navigation.${CPU_ARCH}.yaml up -d
```

# 3. Checking Docker
```
docker logs movensys_navigation_container -f
```

# 4. Get inside Docker
```
nros
```

# 5. Checking URDF 
```
nros ros2 launch movensys_navigation_description movensys_navigation_rviz.launch.py
```