; Auto-generated. Do not edit!


(cl:in-package lstm_motion_model-srv)


;//! \htmlinclude PredictState-request.msg.html

(cl:defclass <PredictState-request> (roslisp-msg-protocol:ros-message)
  ((input_states
    :reader input_states
    :initarg :input_states
    :type (cl:vector lstm_motion_model-msg:State)
   :initform (cl:make-array 0 :element-type 'lstm_motion_model-msg:State :initial-element (cl:make-instance 'lstm_motion_model-msg:State))))
)

(cl:defclass PredictState-request (<PredictState-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PredictState-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PredictState-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lstm_motion_model-srv:<PredictState-request> is deprecated: use lstm_motion_model-srv:PredictState-request instead.")))

(cl:ensure-generic-function 'input_states-val :lambda-list '(m))
(cl:defmethod input_states-val ((m <PredictState-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lstm_motion_model-srv:input_states-val is deprecated.  Use lstm_motion_model-srv:input_states instead.")
  (input_states m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PredictState-request>) ostream)
  "Serializes a message object of type '<PredictState-request>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'input_states))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'input_states))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PredictState-request>) istream)
  "Deserializes a message object of type '<PredictState-request>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'input_states) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'input_states)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'lstm_motion_model-msg:State))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PredictState-request>)))
  "Returns string type for a service object of type '<PredictState-request>"
  "lstm_motion_model/PredictStateRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PredictState-request)))
  "Returns string type for a service object of type 'PredictState-request"
  "lstm_motion_model/PredictStateRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PredictState-request>)))
  "Returns md5sum for a message object of type '<PredictState-request>"
  "def079bdd0ff18cd456b2d37bbf78613")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PredictState-request)))
  "Returns md5sum for a message object of type 'PredictState-request"
  "def079bdd0ff18cd456b2d37bbf78613")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PredictState-request>)))
  "Returns full string definition for message of type '<PredictState-request>"
  (cl:format cl:nil "State[] input_states~%~%================================================================================~%MSG: lstm_motion_model/State~%uint64 id~%float32[] state~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PredictState-request)))
  "Returns full string definition for message of type 'PredictState-request"
  (cl:format cl:nil "State[] input_states~%~%================================================================================~%MSG: lstm_motion_model/State~%uint64 id~%float32[] state~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PredictState-request>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'input_states) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PredictState-request>))
  "Converts a ROS message object to a list"
  (cl:list 'PredictState-request
    (cl:cons ':input_states (input_states msg))
))
;//! \htmlinclude PredictState-response.msg.html

(cl:defclass <PredictState-response> (roslisp-msg-protocol:ros-message)
  ((predicted_states
    :reader predicted_states
    :initarg :predicted_states
    :type (cl:vector lstm_motion_model-msg:State)
   :initform (cl:make-array 0 :element-type 'lstm_motion_model-msg:State :initial-element (cl:make-instance 'lstm_motion_model-msg:State))))
)

(cl:defclass PredictState-response (<PredictState-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PredictState-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PredictState-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lstm_motion_model-srv:<PredictState-response> is deprecated: use lstm_motion_model-srv:PredictState-response instead.")))

(cl:ensure-generic-function 'predicted_states-val :lambda-list '(m))
(cl:defmethod predicted_states-val ((m <PredictState-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lstm_motion_model-srv:predicted_states-val is deprecated.  Use lstm_motion_model-srv:predicted_states instead.")
  (predicted_states m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PredictState-response>) ostream)
  "Serializes a message object of type '<PredictState-response>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'predicted_states))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'predicted_states))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PredictState-response>) istream)
  "Deserializes a message object of type '<PredictState-response>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'predicted_states) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'predicted_states)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'lstm_motion_model-msg:State))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PredictState-response>)))
  "Returns string type for a service object of type '<PredictState-response>"
  "lstm_motion_model/PredictStateResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PredictState-response)))
  "Returns string type for a service object of type 'PredictState-response"
  "lstm_motion_model/PredictStateResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PredictState-response>)))
  "Returns md5sum for a message object of type '<PredictState-response>"
  "def079bdd0ff18cd456b2d37bbf78613")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PredictState-response)))
  "Returns md5sum for a message object of type 'PredictState-response"
  "def079bdd0ff18cd456b2d37bbf78613")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PredictState-response>)))
  "Returns full string definition for message of type '<PredictState-response>"
  (cl:format cl:nil "State[] predicted_states~%~%================================================================================~%MSG: lstm_motion_model/State~%uint64 id~%float32[] state~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PredictState-response)))
  "Returns full string definition for message of type 'PredictState-response"
  (cl:format cl:nil "State[] predicted_states~%~%================================================================================~%MSG: lstm_motion_model/State~%uint64 id~%float32[] state~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PredictState-response>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'predicted_states) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PredictState-response>))
  "Converts a ROS message object to a list"
  (cl:list 'PredictState-response
    (cl:cons ':predicted_states (predicted_states msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'PredictState)))
  'PredictState-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'PredictState)))
  'PredictState-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PredictState)))
  "Returns string type for a service object of type '<PredictState>"
  "lstm_motion_model/PredictState")