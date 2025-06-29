import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    # Command-line arguments
    # tutorial_arg = DeclareLaunchArgument(
    #     "rviz_tutorial", default_value="False", description="Tutorial flag"
    # )

    # db_arg = DeclareLaunchArgument(
    #     "db", default_value="False", description="Database flag"
    # )

    # ros2_control_hardware_type = DeclareLaunchArgument(
    #     "ros2_control_hardware_type",
    #     default_value="mock_components",
    #     description="ROS2 control hardware interface type to use for the launch file -- possible values: [mock_components, isaac]",
    # )

    moveit_config = (
        MoveItConfigsBuilder("custom_robot",package_name="rehab_arm_robot_moveit_config")
        .robot_description(
            file_path="config/rehab_arm_robot.urdf.xacro",
            # mappings={
            #     "ros2_control_hardware_type": LaunchConfiguration(
            #         "ros2_control_hardware_type"
            #     )
            # },
        )
        .robot_description_semantic(file_path="config/rehab_arm_robot.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(
            pipelines=["ompl", "chomp", "pilz_industrial_motion_planner"]
        )
        .to_moveit_configs()
    )

    # Start the actual move_group node/action server
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict()],
        arguments=["--ros-args", "--log-level", "info"],
    )

    # RViz
    # tutorial_mode = LaunchConfiguration("rviz_tutorial")
    rviz_base = os.path.join(
        get_package_share_directory("rehab_arm_robot_moveit_config"), "launch"
    )
    rviz_full_config = os.path.join(rviz_base, "moveit.rviz")
    # rviz_empty_config = os.path.join(rviz_base, "moveit_empty.rviz")
    # rviz_node_tutorial = Node(
    #     package="rviz2",
    #     executable="rviz2",
    #     name="rviz2",
    #     output="log",
    #     arguments=["-d", rviz_empty_config],
    #     parameters=[
    #         moveit_config.robot_description,
    #         moveit_config.robot_description_semantic,
    #         moveit_config.planning_pipelines,
    #         moveit_config.robot_description_kinematics,
    #     ],
    #     condition=IfCondition(tutorial_mode),
    # )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_full_config],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
        ],
        # condition=UnlessCondition(tutorial_mode),
    )

    # Static TF
    static_tf_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        output="log",
        arguments=["0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "world", "dummy_link"],
    )

    # Publish TF
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[moveit_config.robot_description],
    )

    # ros2_control using FakeSystem as hardware
    ros2_controllers_path = os.path.join(
        get_package_share_directory("rehab_arm_robot_moveit_config"),
        "config",
        "ros2_controllers.yaml",
    )
    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[moveit_config.robot_description, ros2_controllers_path],
        remappings=[
            ("/controller_manager/robot_description", "/robot_description"),
        ],
        output="screen",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    rehab_arm_moveit_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["rehab_arm_moveit_controller", "-c", "/controller_manager"],
        output="screen",#dont know the purpose of this line (may research later)
    )

    # # controller spawner of move group
    # panda_arm_controller_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["panda_arm_controller", "-c", "/controller_manager"],
    # )

    # # this is the ee of the panda one so no need to keep it if you dont have ee
    # panda_hand_controller_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["panda_hand_controller", "-c", "/controller_manager"],
    # )

    # # Warehouse mongodb server
    # db_config = LaunchConfiguration("db")
    # mongodb_server_node = Node(
    #     package="warehouse_ros_mongo",
    #     executable="mongo_wrapper_ros.py",
    #     parameters=[
    #         {"warehouse_port": 33829},
    #         {"warehouse_host": "localhost"},
    #         {"warehouse_plugin": "warehouse_ros_mongo::MongoDatabaseConnection"},
    #     ],
    #     output="screen",
    #     condition=IfCondition(db_config),
    # )

    return LaunchDescription(
        [
            # tutorial_arg,
            # db_arg,
            # ros2_control_hardware_type,
            rviz_node,
            # rviz_node_tutorial,
            static_tf_node,
            robot_state_publisher,
            move_group_node,
            ros2_control_node,
            joint_state_broadcaster_spawner,
            rehab_arm_moveit_controller_spawner,
            # panda_hand_controller_spawner,
            # mongodb_server_node,
        ]
    )
