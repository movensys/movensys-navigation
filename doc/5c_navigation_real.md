# Manual 
## Execution Procedure



### Step 1: Run wmx-ros2 for navigation
check `~/workspaces/movensys_ws/src/wmx-ros2/doc/launch_<NAVIGATION_MODEL>_navigation.md` 



### Step 2: Navigation
```
nros ros2 launch movensys_navigation_nav2_config navigation.launch.py
```
add `rsp:=false` if use ros2_control.


### Step 3: Set initial pose
click `2D Pose Estimate` and click the map based on the robot position




### Step 4: Send goal pose
```
nros ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "'{pose: {header: {frame_id: map}, pose: {position: {x: 8.0, y: 0.0, z: 0.0}, \
  orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}}'"
```

