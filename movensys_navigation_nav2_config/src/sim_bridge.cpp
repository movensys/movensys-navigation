// Copyright 2026 Movensys

#include <memory>
#include <string>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "geometry_msgs/msg/twist_stamped.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"

class SimBridge : public rclcpp::Node
{
public:
  SimBridge()
  : Node("sim_bridge")
  {
    this->declare_parameter("kinematic_type", "differential_drive");
    this->declare_parameter<std::vector<std::string>>(
      "wheel_name",
      {"drivewheel_left_joint", "drivewheel_right_joint"});
    this->declare_parameter("wheel_radius", 0.095);
    this->declare_parameter("wheel_to_wheel", 0.55);
    this->declare_parameter("topic_gazebo_commands", "/velocity_controller/commands");
    this->declare_parameter("topic_isaacsim_commands", "/joint_command");
    this->declare_parameter("topic_joint_states", "/joint_states");
    this->declare_parameter("topic_cmd_vel", "/cmd_vel_safe");
    this->declare_parameter("topic_odom_encoder", "/odom_enc");

    kinematic_type_ = this->get_parameter("kinematic_type").as_string();
    wheel_name_ = this->get_parameter("wheel_name").as_string_array();
    wheel_radius_ = this->get_parameter("wheel_radius").as_double();
    wheel_to_wheel_ = this->get_parameter("wheel_to_wheel").as_double();

    omega_motor_.assign(wheel_name_.size(), 0.0);

    auto topic_gazebo_commands = this->get_parameter("topic_gazebo_commands").as_string();
    auto topic_isaacsim_commands = this->get_parameter("topic_isaacsim_commands").as_string();
    auto topic_joint_states = this->get_parameter("topic_joint_states").as_string();
    auto topic_cmd_vel = this->get_parameter("topic_cmd_vel").as_string();
    auto topic_odom_encoder = this->get_parameter("topic_odom_encoder").as_string();

    RCLCPP_INFO(
      this->get_logger(), "Starting sim_bridge (kinematic_type: %s, wheels: %zu)",
      kinematic_type_.c_str(), wheel_name_.size());

    odom_encoder_pub_ = this->create_publisher<nav_msgs::msg::Odometry>(
      topic_odom_encoder, 1);

    gazebo_pub_ = this->create_publisher<std_msgs::msg::Float64MultiArray>(
      topic_gazebo_commands, 1);

    isaacsim_pub_ = this->create_publisher<sensor_msgs::msg::JointState>(
      topic_isaacsim_commands, 1);

    encoder_sub_ = this->create_subscription<sensor_msgs::msg::JointState>(
      topic_joint_states, 1,
      std::bind(&SimBridge::encoderCallback, this, std::placeholders::_1));

    cmd_vel_sub_ = this->create_subscription<geometry_msgs::msg::TwistStamped>(
      topic_cmd_vel, 1,
      std::bind(&SimBridge::cmdVelCallback, this, std::placeholders::_1));
  }

private:
  void encoderCallback(const sensor_msgs::msg::JointState::SharedPtr msg);
  void cmdVelCallback(const geometry_msgs::msg::TwistStamped::SharedPtr msg);

  rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr gazebo_pub_;
  rclcpp::Publisher<sensor_msgs::msg::JointState>::SharedPtr isaacsim_pub_;
  rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr odom_encoder_pub_;
  rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr encoder_sub_;
  rclcpp::Subscription<geometry_msgs::msg::TwistStamped>::SharedPtr cmd_vel_sub_;

  std::string kinematic_type_;
  std::vector<std::string> wheel_name_;
  double wheel_radius_;
  double wheel_to_wheel_;
  std::vector<double> omega_motor_;
};

void SimBridge::cmdVelCallback(const geometry_msgs::msg::TwistStamped::SharedPtr msg)
{
  if (kinematic_type_ == "differential_drive") {
    omega_motor_[0] =
      (2 * msg->twist.linear.x - msg->twist.angular.z * wheel_to_wheel_) /
      (2 * wheel_radius_);

    omega_motor_[1] =
      (2 * msg->twist.linear.x + msg->twist.angular.z * wheel_to_wheel_) /
      (2 * wheel_radius_);
  } else {
    RCLCPP_WARN_ONCE(
      this->get_logger(),
      "Unsupported kinematic_type: %s", kinematic_type_.c_str());
    return;
  }

  // Gazebo: forward velocity command as a Float64MultiArray
  std_msgs::msg::Float64MultiArray motor_data;
  motor_data.data.assign(omega_motor_.begin(), omega_motor_.end());
  gazebo_pub_->publish(motor_data);

  // Isaac Sim: velocity command as a JointState
  sensor_msgs::msg::JointState joint_command;
  joint_command.header.stamp = this->get_clock()->now();
  joint_command.name = wheel_name_;
  joint_command.velocity = omega_motor_;
  isaacsim_pub_->publish(joint_command);
}

void SimBridge::encoderCallback(const sensor_msgs::msg::JointState::SharedPtr msg)
{
  if (wheel_name_.size() < 2) {
    return;
  }

  int index_l = -1;
  int index_r = -1;

  for (size_t i = 0; i < msg->name.size(); i++) {
    if (msg->name[i] == wheel_name_[0]) {
      index_l = i;
    }
    if (msg->name[i] == wheel_name_[1]) {
      index_r = i;
    }
  }

  if (index_l == -1 || index_r == -1) {
    RCLCPP_WARN(this->get_logger(), "Wheel joints not found");
    return;
  }

  double v_r = msg->velocity[index_r] * wheel_radius_;
  double v_l = msg->velocity[index_l] * wheel_radius_;

  auto odom_encoder = nav_msgs::msg::Odometry();
  odom_encoder.header.stamp = this->now();
  odom_encoder.twist.twist.linear.x = (v_r + v_l) / 2.0;
  odom_encoder.twist.twist.linear.y = 0.0;
  odom_encoder.twist.twist.angular.z = (v_r - v_l) / wheel_to_wheel_;

  odom_encoder_pub_->publish(odom_encoder);
}

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<SimBridge>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
