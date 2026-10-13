# SLAM Mapping (HIL)
## Execution Procedure

### Step 1: Open Isaac Sim
`~/workspaces/movensys-simulation/<NAVIGATION_MODEL>/navigation_hil.usd`






### Step 2: Run wmx-r2 for navigation
check `~/workspaces/movensys_ws/src/wmx-r2/doc/launch_differential.md` 
set `use_sim_time:=true`







### Step 3: Mapping
```
nros ros2 launch movensys_navigation_nav2_config mapping.launch.py use_sim_time:=true
```
add `rsp:=false` if use ros2_control. add `use_cuvslam:=true` for use cuvslam.





### Step 4: Run teleop keyboard
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args \
      -p turn:=0.5 \
      -p stamped:=true \
      -p frame_id:=base_link \
      -p use_sim_time:=true \
      -r cmd_vel:=/cmd_vel_safe
```




### Step 5: Saving map
```
nros ros2 run nav2_map_server map_saver_cli -f /home/admin/workspaces/movensys_ws/src/movensys-navigation/movensys_navigation_nav2_config/maps/my_map
```
