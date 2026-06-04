cmake_minimum_required(VERSION 3.8)
project(movensys_navigation_nav2_config)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(sim_bridge src/sim_bridge.cpp)
ament_target_dependencies(sim_bridge
  rclcpp sensor_msgs nav_msgs geometry_msgs std_msgs)

install(TARGETS
  sim_bridge
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY 
  config 
  launch
  rviz
  src
  DESTINATION share/${PROJECT_NAME}/
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
