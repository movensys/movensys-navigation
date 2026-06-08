# Manual 
## Execution Procedure

### Step 1: Navigation
```
nros ros2 launch movensys_navigation_nav2_config navigation.launch.py use_sim_time:=true rsp:=false
```
> For the Isaac Sim option (not Gazebo), use `rsp:=true` (default) instead — Isaac does not publish `/robot_description`.



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



### Step 4: Set initial pose
click `2D Pose Estimate` and click the map based on the robot position




### Step 5: Send goal pose
```
nros ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "'{pose: {header: {frame_id: map}, pose: {position: {x: 8.0, y: 0.0, z: 0.0}, \
  orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}}'"
```

