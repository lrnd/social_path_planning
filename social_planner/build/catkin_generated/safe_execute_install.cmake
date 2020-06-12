execute_process(COMMAND "/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/build/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/build/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
