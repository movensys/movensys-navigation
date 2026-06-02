# Manual 
## Execution Procedure

### Step 1a: Open Isaac Sim
`~/workspaces/movensys-simulation/<NAVIGATION_MODEL>/navigation.usd`

### Step 1b: Open Gazebo
```
nros ros2 launch movensys_navigation_description gazebo_navigation_simulation.launch.py
```




### Step 2a: Run simulator bridge
```
nros ros2 launch movensys_navigation_nav2 sim_bridge.launch.py simulator:=isaacsim use_sim_time:=true 
```
`simulator:=gazebo` for use gazebo





### Step 3a: Run teleop keyboard
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard use_sim_time:=true
```





