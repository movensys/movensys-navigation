# Manual 
## Execution Procedure

### Step 1: Run EKF + RSB
```
nros ros2 launch movensys_navigation_nav2_config base.launch.py use_sim_time:=true 
```



### Step 2a: Open Isaac Sim
`~/workspaces/movensys-simulation/<NAVIGATION_MODEL>/navigation_hil.usd`







### Step 3: Run wmx-ros2 for navigation
check `~/workspaces/movensys_ws/src/wmx-ros2/doc/launch_<NAVIGATION_MODEL>_navigation.md` 
set `use_sim_time:=true`







### Step 4: Run teleop keyboard
```
nros ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p turn:=0.5
```





