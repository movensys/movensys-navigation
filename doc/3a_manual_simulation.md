# Manual 
## Execution Procedure


### Step 1a: Open Isaac Sim
`~/workspaces/movensys-simulation/<NAVIGATION_MODEL>/navigation_simulation.usd`

### Step 1b: Open Gazebo
```
nros ros2 launch movensys_navigation_description gazebo_navigation_simulation.launch.py
```




### Step 2: Run simulator bridge
```
nros ros2 launch movensys_navigation_nav2_config sim_bridge.launch.py use_sim_time:=true 
```






### Step 3: Run EKF + RSP
```
nros ros2 launch movensys_navigation_nav2_config base.launch.py use_sim_time:=true 
```
add `rsp:=false` if use gazebo (step 1b) and add `use_cuvslam:=true` for use cuvslam.







### Step 4: Run teleop keyboard
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args \
      -p turn:=0.5 \
      -p stamped:=true \
      -p frame_id:=base_link \
      -p use_sim_time:=true \
      -r cmd_vel:=/cmd_vel_safe
```





