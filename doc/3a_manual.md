# Manual 
## Execution Procedure

### Step 1: Run EKF + RSB
```
nros ros2 launch movensys_navigation_nav2_config base.launch.py use_sim_time:=true 
```



### Step 2a: Open Isaac Sim


### Step 2b: Open Gazebo
```
nros ros2 launch movensys_navigation_description gazebo_navigation_simulation.launch.py
```






### Step 3: Run simulator bridge
```
nros ros2 launch movensys_navigation_nav2_config sim_bridge.launch.py use_sim_time:=true 
```







### Step 4: Run teleop keyboard
```
nros ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p turn:=0.5
```





