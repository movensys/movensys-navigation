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





### Step 3: Navigation
```
nros ros2 launch movensys_navigation_nav2_config navigation.launch.py use_sim_time:=true
```
add `rsp:=false` if use gazebo (step 1b).






### Step 4: Set initial pose
click `2D Pose Estimate` and click the map based on the robot position




### Step 5: Send goal pose
```
nros ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "'{pose: {header: {frame_id: map}, pose: {position: {x: 8.0, y: 0.0, z: 0.0}, \
  orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}}'"
```

