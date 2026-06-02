cmake_minimum_required(VERSION 3.8)
project(navigation_package)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)

# --- differential_drive_gazebo_bridge ---
add_executable(differential_drive_gazebo_bridge src/differential_drive_gazebo_bridge.cpp)
ament_target_dependencies(differential_drive_gazebo_bridge
  rclcpp sensor_msgs nav_msgs geometry_msgs std_msgs)

install(TARGETS
  differential_drive_gazebo_bridge
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY config launch
  DESTINATION share/${PROJECT_NAME}/
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
