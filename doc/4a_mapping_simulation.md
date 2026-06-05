# Manual 
## Execution Procedure

### Step 1: Mapping
```
nros ros2 launch movensys_navigation_nav2_config mapping.launch.py use_sim_time:=true 
```



### Step 2a: Open Isaac Sim
`~/workspaces/movensys-simulation/<NAVIGATION_MODEL>/navigation_simulation.usd`

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




### Step 5: Saving map
```
nros ros2 run nav2_map_server map_saver_cli -f /home/admin/workspaces/movensys_ws/src/movensys-navigation/movensys_navigation_nav2_config/maps/my_map
```





