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

# --- gRPC / Protobuf ---
find_package(Protobuf REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(GRPCPP REQUIRED grpc++ IMPORTED_TARGET)
find_program(GRPC_CPP_PLUGIN grpc_cpp_plugin REQUIRED)

set(PROTO_FILE "${CMAKE_CURRENT_SOURCE_DIR}/proto/robot.proto")
set(PROTO_OUT  "${CMAKE_CURRENT_BINARY_DIR}")

set(PROTO_SRCS "${PROTO_OUT}/robot.pb.cc")
set(PROTO_HDRS "${PROTO_OUT}/robot.pb.h")
set(GRPC_SRCS  "${PROTO_OUT}/robot.grpc.pb.cc")
set(GRPC_HDRS  "${PROTO_OUT}/robot.grpc.pb.h")

add_custom_command(
  OUTPUT ${PROTO_SRCS} ${PROTO_HDRS} ${GRPC_SRCS} ${GRPC_HDRS}
  COMMAND ${Protobuf_PROTOC_EXECUTABLE}
    --cpp_out  ${PROTO_OUT}
    --grpc_out ${PROTO_OUT}
    --plugin=protoc-gen-grpc=${GRPC_CPP_PLUGIN}
    -I ${CMAKE_CURRENT_SOURCE_DIR}/proto
    ${PROTO_FILE}
  DEPENDS ${PROTO_FILE}
)

# --- differential_drive ---
add_executable(differential_drive src/differential_drive.cpp)
ament_target_dependencies(differential_drive
  rclcpp sensor_msgs nav_msgs geometry_msgs std_msgs)

# --- safe_motion ---
add_executable(safe_motion src/safe_motion.cpp)
ament_target_dependencies(safe_motion
  rclcpp geometry_msgs)

# --- grpc_bridge ---
add_executable(grpc_bridge
  src/grpc_bridge.cpp
  ${PROTO_SRCS}
  ${GRPC_SRCS}
)
target_include_directories(grpc_bridge PRIVATE ${PROTO_OUT})
target_link_libraries(grpc_bridge
  protobuf::libprotobuf
  PkgConfig::GRPCPP
)
ament_target_dependencies(grpc_bridge
  rclcpp nav_msgs geometry_msgs)

install(TARGETS
  differential_drive
  safe_motion
  grpc_bridge
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
