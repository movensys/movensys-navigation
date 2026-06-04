#include <memory>
#include <string>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"

class DifferentialDrive : public rclcpp::Node{
public:
    DifferentialDrive() : Node("differential_drive")
    {
        this->declare_parameter("wheel_left_name", "wheel_l_joint");
        this->declare_parameter("wheel_right_name", "wheel_r_joint");
        this->declare_parameter("wheel_radius", 0.09);
        this->declare_parameter("wheel_to_wheel", 0.24);
        this->declare_parameter("topic_cmd_vel_safe", "/cmd_vel_safe");
        this->declare_parameter("topic_joint_states", "/joint_states");
        this->declare_parameter("topic_odom_encoder", "/odom_encoder");
        this->declare_parameter("topic_motor_commands", "/velocity_controller/commands");

        wheel_left_name_ = this->get_parameter("wheel_left_name").as_string();
        wheel_right_name_ = this->get_parameter("wheel_right_name").as_string();
        wheel_radius_ = this->get_parameter("wheel_radius").as_double();
        wheel_to_wheel_ = this->get_parameter("wheel_to_wheel").as_double();

        auto topic_cmd_vel_safe   = this->get_parameter("topic_cmd_vel_safe").as_string();
        auto topic_joint_states   = this->get_parameter("topic_joint_states").as_string();
        auto topic_odom_encoder   = this->get_parameter("topic_odom_encoder").as_string();
        auto topic_motor_commands = this->get_parameter("topic_motor_commands").as_string();

        odom_encoder_pub_ = this->create_publisher<nav_msgs::msg::Odometry>(
            topic_odom_encoder, 1);

        motor_pub_ = this->create_publisher<std_msgs::msg::Float64MultiArray>(
            topic_motor_commands, 1);

        encoder_sub_ = this->create_subscription<sensor_msgs::msg::JointState>(
            topic_joint_states, 1,
            std::bind(&DifferentialDrive::encoderCallback, this, std::placeholders::_1));

        command_velocity_safe_sub_ = this->create_subscription<geometry_msgs::msg::Twist>(
            topic_cmd_vel_safe, 1,
            std::bind(&DifferentialDrive::cmdVelSafeCallback, this, std::placeholders::_1));
    }

private:
    void encoderCallback(const sensor_msgs::msg::JointState::SharedPtr msg);
    void cmdVelSafeCallback(const geometry_msgs::msg::Twist::SharedPtr msg);

    rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr motor_pub_;
    rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr odom_encoder_pub_;
    rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr encoder_sub_;
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr command_velocity_safe_sub_;

    std::string wheel_left_name_;
    std::string wheel_right_name_;
    double wheel_radius_;
    double wheel_to_wheel_;
    double omega_left_motor_;
    double omega_right_motor_;
};

void DifferentialDrive::cmdVelSafeCallback(const geometry_msgs::msg::Twist::SharedPtr msg){
    omega_left_motor_ =
        (2 * msg->linear.x - msg->angular.z * wheel_to_wheel_) /
        (2 * wheel_radius_);

    omega_right_motor_ =
        (2 * msg->linear.x + msg->angular.z * wheel_to_wheel_) /
        (2 * wheel_radius_);

    std_msgs::msg::Float64MultiArray motor_data;

    motor_data.data.push_back(omega_left_motor_);
    motor_data.data.push_back(omega_right_motor_);

    motor_pub_->publish(motor_data);
}

void DifferentialDrive::encoderCallback(const sensor_msgs::msg::JointState::SharedPtr msg){
    int index_l = -1;
    int index_r = -1;

    for (size_t i = 0; i < msg->name.size(); i++){
        if (msg->name[i] == wheel_left_name_)
            index_l = i;
        if (msg->name[i] == wheel_right_name_)
            index_r = i;
    }

    if (index_l == -1 || index_r == -1){
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
    auto node = std::make_shared<DifferentialDrive>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
