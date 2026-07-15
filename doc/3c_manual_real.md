# Manual 
## Execution Procedure

### Step 1: Run wmx-r2 for navigation
check `~/workspaces/movensys_ws/src/wmx-r2/doc/launch_<NAVIGATION_MODEL>_navigation.md` 





### Step 2: Run EKF + RSB
```
nros ros2 launch movensys_navigation_nav2_config base.launch.py
```
add `rsp:=false` if use ros2_control.







### Step 3: Run teleop keyboard
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args \
      -p turn:=0.5 \
      -p stamped:=true \
      -p frame_id:=base_link \
      -r cmd_vel:=/cmd_vel_safe
```





