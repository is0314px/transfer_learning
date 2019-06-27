# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "egpsr: 1 messages, 0 services")

set(MSG_I_FLAGS "-Iegpsr:/home/emlab/catkin_robocup/src/egpsr_ros/egpsr/msg;-Istd_msgs:/opt/ros/indigo/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(egpsr_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/emlab/catkin_robocup/src/egpsr_ros/egpsr/msg/EgpsrMsg.msg" NAME_WE)
add_custom_target(_egpsr_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "egpsr" "/home/emlab/catkin_robocup/src/egpsr_ros/egpsr/msg/EgpsrMsg.msg" ""
)

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(egpsr
  "/home/emlab/catkin_robocup/src/egpsr_ros/egpsr/msg/EgpsrMsg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/egpsr
)

### Generating Services

### Generating Module File
_generate_module_cpp(egpsr
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/egpsr
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(egpsr_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(egpsr_generate_messages egpsr_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/emlab/catkin_robocup/src/egpsr_ros/egpsr/msg/EgpsrMsg.msg" NAME_WE)
add_dependencies(egpsr_generate_messages_cpp _egpsr_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(egpsr_gencpp)
add_dependencies(egpsr_gencpp egpsr_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS egpsr_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(egpsr
  "/home/emlab/catkin_robocup/src/egpsr_ros/egpsr/msg/EgpsrMsg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/egpsr
)

### Generating Services

### Generating Module File
_generate_module_lisp(egpsr
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/egpsr
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(egpsr_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(egpsr_generate_messages egpsr_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/emlab/catkin_robocup/src/egpsr_ros/egpsr/msg/EgpsrMsg.msg" NAME_WE)
add_dependencies(egpsr_generate_messages_lisp _egpsr_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(egpsr_genlisp)
add_dependencies(egpsr_genlisp egpsr_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS egpsr_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(egpsr
  "/home/emlab/catkin_robocup/src/egpsr_ros/egpsr/msg/EgpsrMsg.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/egpsr
)

### Generating Services

### Generating Module File
_generate_module_py(egpsr
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/egpsr
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(egpsr_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(egpsr_generate_messages egpsr_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/emlab/catkin_robocup/src/egpsr_ros/egpsr/msg/EgpsrMsg.msg" NAME_WE)
add_dependencies(egpsr_generate_messages_py _egpsr_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(egpsr_genpy)
add_dependencies(egpsr_genpy egpsr_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS egpsr_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/egpsr)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/egpsr
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(egpsr_generate_messages_cpp std_msgs_generate_messages_cpp)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/egpsr)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/egpsr
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(egpsr_generate_messages_lisp std_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/egpsr)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/egpsr\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/egpsr
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(egpsr_generate_messages_py std_msgs_generate_messages_py)
