# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "lstm_motion_model: 2 messages, 2 services")

set(MSG_I_FLAGS "-Ilstm_motion_model:/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(lstm_motion_model_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/PredictState.srv" NAME_WE)
add_custom_target(_lstm_motion_model_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "lstm_motion_model" "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/PredictState.srv" "lstm_motion_model/State"
)

get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg" NAME_WE)
add_custom_target(_lstm_motion_model_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "lstm_motion_model" "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg" ""
)

get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/ManageModels.srv" NAME_WE)
add_custom_target(_lstm_motion_model_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "lstm_motion_model" "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/ManageModels.srv" "lstm_motion_model/ModelManagement"
)

get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg" NAME_WE)
add_custom_target(_lstm_motion_model_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "lstm_motion_model" "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/lstm_motion_model
)
_generate_msg_cpp(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/lstm_motion_model
)

### Generating Services
_generate_srv_cpp(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/PredictState.srv"
  "${MSG_I_FLAGS}"
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/lstm_motion_model
)
_generate_srv_cpp(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/ManageModels.srv"
  "${MSG_I_FLAGS}"
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/lstm_motion_model
)

### Generating Module File
_generate_module_cpp(lstm_motion_model
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/lstm_motion_model
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(lstm_motion_model_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(lstm_motion_model_generate_messages lstm_motion_model_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/PredictState.srv" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_cpp _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_cpp _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/ManageModels.srv" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_cpp _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_cpp _lstm_motion_model_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(lstm_motion_model_gencpp)
add_dependencies(lstm_motion_model_gencpp lstm_motion_model_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS lstm_motion_model_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/lstm_motion_model
)
_generate_msg_eus(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/lstm_motion_model
)

### Generating Services
_generate_srv_eus(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/PredictState.srv"
  "${MSG_I_FLAGS}"
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/lstm_motion_model
)
_generate_srv_eus(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/ManageModels.srv"
  "${MSG_I_FLAGS}"
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/lstm_motion_model
)

### Generating Module File
_generate_module_eus(lstm_motion_model
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/lstm_motion_model
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(lstm_motion_model_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(lstm_motion_model_generate_messages lstm_motion_model_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/PredictState.srv" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_eus _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_eus _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/ManageModels.srv" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_eus _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_eus _lstm_motion_model_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(lstm_motion_model_geneus)
add_dependencies(lstm_motion_model_geneus lstm_motion_model_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS lstm_motion_model_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/lstm_motion_model
)
_generate_msg_lisp(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/lstm_motion_model
)

### Generating Services
_generate_srv_lisp(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/PredictState.srv"
  "${MSG_I_FLAGS}"
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/lstm_motion_model
)
_generate_srv_lisp(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/ManageModels.srv"
  "${MSG_I_FLAGS}"
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/lstm_motion_model
)

### Generating Module File
_generate_module_lisp(lstm_motion_model
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/lstm_motion_model
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(lstm_motion_model_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(lstm_motion_model_generate_messages lstm_motion_model_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/PredictState.srv" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_lisp _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_lisp _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/ManageModels.srv" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_lisp _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_lisp _lstm_motion_model_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(lstm_motion_model_genlisp)
add_dependencies(lstm_motion_model_genlisp lstm_motion_model_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS lstm_motion_model_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/lstm_motion_model
)
_generate_msg_nodejs(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/lstm_motion_model
)

### Generating Services
_generate_srv_nodejs(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/PredictState.srv"
  "${MSG_I_FLAGS}"
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/lstm_motion_model
)
_generate_srv_nodejs(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/ManageModels.srv"
  "${MSG_I_FLAGS}"
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/lstm_motion_model
)

### Generating Module File
_generate_module_nodejs(lstm_motion_model
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/lstm_motion_model
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(lstm_motion_model_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(lstm_motion_model_generate_messages lstm_motion_model_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/PredictState.srv" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_nodejs _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_nodejs _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/ManageModels.srv" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_nodejs _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_nodejs _lstm_motion_model_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(lstm_motion_model_gennodejs)
add_dependencies(lstm_motion_model_gennodejs lstm_motion_model_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS lstm_motion_model_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/lstm_motion_model
)
_generate_msg_py(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/lstm_motion_model
)

### Generating Services
_generate_srv_py(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/PredictState.srv"
  "${MSG_I_FLAGS}"
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/lstm_motion_model
)
_generate_srv_py(lstm_motion_model
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/ManageModels.srv"
  "${MSG_I_FLAGS}"
  "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/lstm_motion_model
)

### Generating Module File
_generate_module_py(lstm_motion_model
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/lstm_motion_model
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(lstm_motion_model_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(lstm_motion_model_generate_messages lstm_motion_model_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/PredictState.srv" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_py _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/ModelManagement.msg" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_py _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/srv/ManageModels.srv" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_py _lstm_motion_model_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg/State.msg" NAME_WE)
add_dependencies(lstm_motion_model_generate_messages_py _lstm_motion_model_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(lstm_motion_model_genpy)
add_dependencies(lstm_motion_model_genpy lstm_motion_model_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS lstm_motion_model_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/lstm_motion_model)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/lstm_motion_model
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(lstm_motion_model_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/lstm_motion_model)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/lstm_motion_model
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(lstm_motion_model_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/lstm_motion_model)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/lstm_motion_model
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(lstm_motion_model_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/lstm_motion_model)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/lstm_motion_model
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(lstm_motion_model_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/lstm_motion_model)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/lstm_motion_model\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/lstm_motion_model
    DESTINATION ${genpy_INSTALL_DIR}
    # skip all init files
    PATTERN "__init__.py" EXCLUDE
    PATTERN "__init__.pyc" EXCLUDE
  )
  # install init files which are not in the root folder of the generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/lstm_motion_model
    DESTINATION ${genpy_INSTALL_DIR}
    FILES_MATCHING
    REGEX "${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/lstm_motion_model/.+/__init__.pyc?$"
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(lstm_motion_model_generate_messages_py std_msgs_generate_messages_py)
endif()
