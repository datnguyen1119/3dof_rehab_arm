cmake_minimum_required(VERSION 3.5)
project(rehab_arm_robot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
#find_package(xacro REQUIRED)

install(DIRECTORY
  meshes
  urdf
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

