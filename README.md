# Movensys Navigation

ROS 2 packages, Docker compose configs, and end-to-end examples for driving a
differential-drive mobile base with the
[WMX R2](https://github.com/movensys/wmx-r2) motion control stack and the
[Nav2](https://docs.nav2.org/) navigation framework, on top of either Gazebo or
[NVIDIA Isaac Sim](https://github.com/movensys/movensys-simulation).

## Overview

This repository is a ROS 2 workspace package set that pairs the WMX motion
engine with a Nav2-based navigation and localization stack. Nav2 plans and
follows paths; WMX turns the resulting velocity commands into deterministic
wheel motion over EtherCAT. It supports three execution modes for every
example:

- **Simulation** — pure simulation (Isaac Sim or Gazebo), no hardware
- **SIL** — simulation-in-the-loop, simulator visuals + real WMX runtime
- **Real** — control of the real base via WMX over EtherCAT

The included examples cover manual (teleop) driving, SLAM map building with
SLAM Toolbox, and autonomous navigation with Nav2 against a saved map.

## Repository Layout

```
.
├── movensys_navigation_description/   # URDF, meshes, Gazebo world & RViz launch
├── movensys_navigation_nav2_config/   # Nav2 params, EKF, SLAM, sim bridge, launches
├── movensys_navigation_perception/    # Sensor bring-up for the real base
├── docker/                            # Compose stacks and Dockerfiles
└── doc/                               # Step-by-step example walkthroughs
```

## Packages

| Package | Description |
|---------|-------------|
| `movensys_navigation_description`  | URDF/xacro, meshes, Gazebo world, and RViz bring-up for the `diffbot` differential-drive base |
| `movensys_navigation_nav2_config`  | Nav2 configuration (planner, controller, behavior tree, AMCL), the `robot_localization` EKF, SLAM Toolbox config, the `sim_bridge` node, and the `base` / `mapping` / `navigation` launches |
| `movensys_navigation_perception`   | Sensor bring-up (LiDAR / depth) for localization and obstacle avoidance on the real base |

Velocity commands reach the wheels through the
[WMX R2](https://github.com/movensys/wmx-r2) differential-drive controller
(consuming `/cmd_vel_safe`) over EtherCAT; see that repository for the
underlying motion-control nodes and the base bring-up
(`launch_<NAVIGATION_MODEL>_navigation.md`).

## Examples

Each example has a dedicated walkthrough under [`doc/`](doc/). The numbered
prefix selects the scenario; the trailing letter selects the execution mode.

| #  | Scenario                | Simulation                                   | SIL                                   | Real                                   |
|----|-------------------------|----------------------------------------------|---------------------------------------|----------------------------------------|
| 3  | Manual driving          | [3a](doc/3a_manual_simulation.md)            | [3b](doc/3b_manual_hil.md)            | [3c](doc/3c_manual_real.md)            |
| 4  | SLAM mapping            | [4a](doc/4a_mapping_simulation.md)           | [4b](doc/4b_mapping_hil.md)           | [4c](doc/4c_mapping_real.md)           |
| 5  | Autonomous navigation   | [5a](doc/5a_navigation_simulation.md)        | [5b](doc/5b_navigation_hil.md)        | [5c](doc/5c_navigation_real.md)        |

Host-setup guides (`doc/1_setup.md`, `doc/2_docker.md`) are also provided.

## Requirements

- Ubuntu 22.04 or 24.04
- ROS 2 Humble or Jazzy
- Docker with `docker compose` (the workspace runs inside a container)
- An NVIDIA GPU and Isaac ROS prerequisites for the `isaac-ros_*` images
  (see the [Isaac ROS getting-started guide](https://nvidia-isaac-ros.github.io/getting_started/index.html))
- The [`movensys-simulation`](https://github.com/movensys/movensys-simulation) repo for Isaac Sim scenes

## Quick Start

### 1. Configure the host environment

Add the following to your `~/.bashrc` (adjust the variables for your setup):

```
export ROS_DOMAIN_ID=73                         # any free domain id
export ROS_DISTRO=jazzy                         # {jazzy, humble}
export CPU_ARCH=amd64                           # {amd64, arm64}
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

export MOVENSYS_ROS_VERSION=isaac-ros_4.1       # {general, isaac-ros_4.1, isaac-ros_3.2}
export NAVIGATION_MODEL=diffbot                 # {diffbot}

source ~/workspaces/movensys_ws/src/movensys-navigation/docker/nros.bash
```

```
xhost +local:docker
source ~/.bashrc
```

### 2. Raise CycloneDDS socket buffers

```
sudo tee /etc/sysctl.d/99-network-buffers.conf << 'EOF'
net.core.rmem_max=67108864
net.core.rmem_default=67108864
net.core.wmem_max=67108864
net.core.wmem_default=67108864
EOF

sudo sysctl -p /etc/sysctl.d/99-network-buffers.conf
```

### 3. Clone the repository

```
mkdir -p ~/workspaces/movensys_ws/src
cd ~/workspaces/movensys_ws/src
git clone https://github.com/movensys/movensys-navigation.git
```

### 4. Build and start the container

```
cd ~/workspaces/movensys_ws/src/movensys-navigation/docker
docker compose -f ${MOVENSYS_ROS_VERSION}.yaml -f movensys_navigation.${CPU_ARCH}.yaml down
docker compose -f ${MOVENSYS_ROS_VERSION}.yaml -f movensys_navigation.${CPU_ARCH}.yaml build
docker compose -f ${MOVENSYS_ROS_VERSION}.yaml -f movensys_navigation.${CPU_ARCH}.yaml up -d
```

Verify the container is healthy:

```
docker logs movensys_navigation_container -f
```

Enter the container shell:

```
nros
```

### 5. Run an example

Pick a walkthrough from the table above (for instance,
[`doc/3a_manual_simulation.md`](doc/3a_manual_simulation.md)) and follow its
steps. A typical run is: open the matching scene from `movensys-simulation` in
Isaac Sim (or launch Gazebo), start the sim bridge, launch the base (or mapping
/ navigation), and drive or send a goal pose.

## Related Repositories

- [wmx-r2](https://github.com/movensys/wmx-r2) — Core WMX R2 motion control packages
- [wmx-r2-doc](https://github.com/movensys/wmx-r2-doc) — Documentation site for the WMX R2 stack
- [movensys-simulation](https://github.com/movensys/movensys-simulation) — Isaac Sim USD scenes used by the examples here

## License

Released under the MIT License. See [`LICENSE`](LICENSE) for details.
