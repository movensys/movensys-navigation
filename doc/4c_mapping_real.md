# Manual 
## Execution Procedure




### Step 1: Run wmx-ros2 for navigation
check `~/workspaces/movensys_ws/src/wmx-ros2/doc/launch_<NAVIGATION_MODEL>_navigation.md` 







### Step 2: Mapping
```
nros ros2 launch movensys_navigation_nav2_config mapping.launch.py
```





### Step 3: Run teleop keyboard
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args \
      -p turn:=0.5 \
      -p stamped:=true \
      -p frame_id:=base_link \
      -r cmd_vel:=/cmd_vel_safe
```




### Step 4: Saving map
```
nros ros2 run nav2_map_server map_saver_cli -f /home/admin/workspaces/movensys_ws/src/movensys-navigation/movensys_navigation_nav2_config/maps/my_map
```
