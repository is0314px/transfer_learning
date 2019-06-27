# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "human_navigation: 3 messages, 0 services")

set(MSG_I_FLAGS "-Ihuman_navigation:/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg;-Istd_msgs:/opt/ros/indigo/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/indigo/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(human_navigation_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/ObjectInfo.msg" NAME_WE)
add_custom_target(_human_navigation_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "human_navigation" "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/ObjectInfo.msg" "geometry_msgs/Point"
)

get_filename_component(_filename "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/TaskInfo.msg" NAME_WE)
add_custom_target(_human_navigation_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "human_navigation" "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/TaskInfo.msg" "geometry_msgs/Point:human_navigation/ObjectInfo"
)

get_filename_component(_filename "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/HumanNaviMsg.msg" NAME_WE)
add_custom_target(_human_navigation_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "human_navigation" "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/HumanNaviMsg.msg" ""
)

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(human_navigation
  "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/ObjectInfo.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/human_navigation
)
_generate_msg_cpp(human_navigation
  "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/TaskInfo.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Point.msg;/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/ObjectInfo.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/human_navigation
)
_generate_msg_cpp(human_navigation
  "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/HumanNaviMsg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/human_navigation
)

### Generating Services

### Generating Module File
_generate_module_cpp(human_navigation
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/human_navigation
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(human_navigation_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(human_navigation_generate_messages human_navigation_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/ObjectInfo.msg" NAME_WE)
add_dependencies(human_navigation_generate_messages_cpp _human_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/TaskInfo.msg" NAME_WE)
add_dependencies(human_navigation_generate_messages_cpp _human_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/HumanNaviMsg.msg" NAME_WE)
add_dependencies(human_navigation_generate_messages_cpp _human_navigation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(human_navigation_gencpp)
add_dependencies(human_navigation_gencpp human_navigation_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS human_navigation_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(human_navigation
  "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/ObjectInfo.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/human_navigation
)
_generate_msg_lisp(human_navigation
  "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/TaskInfo.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Point.msg;/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/ObjectInfo.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/human_navigation
)
_generate_msg_lisp(human_navigation
  "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/HumanNaviMsg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/human_navigation
)

### Generating Services

### Generating Module File
_generate_module_lisp(human_navigation
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/human_navigation
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(human_navigation_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(human_navigation_generate_messages human_navigation_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/ObjectInfo.msg" NAME_WE)
add_dependencies(human_navigation_generate_messages_lisp _human_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/TaskInfo.msg" NAME_WE)
add_dependencies(human_navigation_generate_messages_lisp _human_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/HumanNaviMsg.msg" NAME_WE)
add_dependencies(human_navigation_generate_messages_lisp _human_navigation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(human_navigation_genlisp)
add_dependencies(human_navigation_genlisp human_navigation_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS human_navigation_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(human_navigation
  "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/ObjectInfo.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/human_navigation
)
_generate_msg_py(human_navigation
  "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/TaskInfo.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Point.msg;/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/ObjectInfo.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/human_navigation
)
_generate_msg_py(human_navigation
  "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/HumanNaviMsg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/human_navigation
)

### Generating Services

### Generating Module File
_generate_module_py(human_navigation
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/human_navigation
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(human_navigation_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(human_navigation_generate_messages human_navigation_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/ObjectInfo.msg" NAME_WE)
add_dependencies(human_navigation_generate_messages_py _human_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/TaskInfo.msg" NAME_WE)
add_dependencies(human_navigation_generate_messages_py _human_navigation_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg/HumanNaviMsg.msg" NAME_WE)
add_dependencies(human_navigation_generate_messages_py _human_navigation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(human_navigation_genpy)
add_dependencies(human_navigation_genpy human_navigation_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS human_navigation_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/human_navigation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/human_navigation
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(human_navigation_generate_messages_cpp std_msgs_generate_messages_cpp)
add_dependencies(human_navigation_generate_messages_cpp geometry_msgs_generate_messages_cpp)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/human_navigation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/human_navigation
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(human_navigation_generate_messages_lisp std_msgs_generate_messages_lisp)
add_dependencies(human_navigation_generate_messages_lisp geometry_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/human_navigation)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/human_navigation\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/human_navigation
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(human_navigation_generate_messages_py std_msgs_generate_messages_py)
add_dependencies(human_navigation_generate_messages_py geometry_msgs_generate_messages_py)
