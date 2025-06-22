cmake_minimum_required(VERSION 3.8)
project(unitree_robot_description)

# 默认使用 C++17（可选）
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

# 查找 ROS 2 和依赖包
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# 安装 URDF/Xacro 文件到 share/
install(
  DIRECTORY urdf meshes rviz launch
  DESTINATION share/${PROJECT_NAME}
)

# 安装 launch 文件
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# 启用测试（可选）
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

# 生成包配置
ament_package()