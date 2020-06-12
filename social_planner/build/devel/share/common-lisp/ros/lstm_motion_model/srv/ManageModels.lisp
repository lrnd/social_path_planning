; Auto-generated. Do not edit!


(cl:in-package lstm_motion_model-srv)


;//! \htmlinclude ManageModels-request.msg.html

(cl:defclass <ManageModels-request> (roslisp-msg-protocol:ros-message)
  ((management_requests
    :reader management_requests
    :initarg :management_requests
    :type (cl:vector lstm_motion_model-msg:ModelManagement)
   :initform (cl:make-array 0 :element-type 'lstm_motion_model-msg:ModelManagement :initial-element (cl:make-instance 'lstm_motion_model-msg:ModelManagement))))
)

(cl:defclass ManageModels-request (<ManageModels-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ManageModels-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ManageModels-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lstm_motion_model-srv:<ManageModels-request> is deprecated: use lstm_motion_model-srv:ManageModels-request instead.")))

(cl:ensure-generic-function 'management_requests-val :lambda-list '(m))
(cl:defmethod management_requests-val ((m <ManageModels-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lstm_motion_model-srv:management_requests-val is deprecated.  Use lstm_motion_model-srv:management_requests instead.")
  (management_requests m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ManageModels-request>) ostream)
  "Serializes a message object of type '<ManageModels-request>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'management_requests))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'management_requests))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ManageModels-request>) istream)
  "Deserializes a message object of type '<ManageModels-request>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'management_requests) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'management_requests)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'lstm_motion_model-msg:ModelManagement))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ManageModels-request>)))
  "Returns string type for a service object of type '<ManageModels-request>"
  "lstm_motion_model/ManageModelsRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ManageModels-request)))
  "Returns string type for a service object of type 'ManageModels-request"
  "lstm_motion_model/ManageModelsRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ManageModels-request>)))
  "Returns md5sum for a message object of type '<ManageModels-request>"
  "bdd8f71f894accd0c4b5f9c68c657241")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ManageModels-request)))
  "Returns md5sum for a message object of type 'ManageModels-request"
  "bdd8f71f894accd0c4b5f9c68c657241")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ManageModels-request>)))
  "Returns full string definition for message of type '<ManageModels-request>"
  (cl:format cl:nil "ModelManagement[] management_requests~%~%================================================================================~%MSG: lstm_motion_model/ModelManagement~%uint64 id~%uint16 action~%uint16 NEW=0~%uint16 COPY=1~%uint16 DELETE=2~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ManageModels-request)))
  "Returns full string definition for message of type 'ManageModels-request"
  (cl:format cl:nil "ModelManagement[] management_requests~%~%================================================================================~%MSG: lstm_motion_model/ModelManagement~%uint64 id~%uint16 action~%uint16 NEW=0~%uint16 COPY=1~%uint16 DELETE=2~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ManageModels-request>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'management_requests) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ManageModels-request>))
  "Converts a ROS message object to a list"
  (cl:list 'ManageModels-request
    (cl:cons ':management_requests (management_requests msg))
))
;//! \htmlinclude ManageModels-response.msg.html

(cl:defclass <ManageModels-response> (roslisp-msg-protocol:ros-message)
  ((management_responses
    :reader management_responses
    :initarg :management_responses
    :type (cl:vector lstm_motion_model-msg:ModelManagement)
   :initform (cl:make-array 0 :element-type 'lstm_motion_model-msg:ModelManagement :initial-element (cl:make-instance 'lstm_motion_model-msg:ModelManagement))))
)

(cl:defclass ManageModels-response (<ManageModels-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ManageModels-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ManageModels-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lstm_motion_model-srv:<ManageModels-response> is deprecated: use lstm_motion_model-srv:ManageModels-response instead.")))

(cl:ensure-generic-function 'management_responses-val :lambda-list '(m))
(cl:defmethod management_responses-val ((m <ManageModels-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lstm_motion_model-srv:management_responses-val is deprecated.  Use lstm_motion_model-srv:management_responses instead.")
  (management_responses m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ManageModels-response>) ostream)
  "Serializes a message object of type '<ManageModels-response>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'management_responses))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'management_responses))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ManageModels-response>) istream)
  "Deserializes a message object of type '<ManageModels-response>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'management_responses) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'management_responses)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'lstm_motion_model-msg:ModelManagement))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ManageModels-response>)))
  "Returns string type for a service object of type '<ManageModels-response>"
  "lstm_motion_model/ManageModelsResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ManageModels-response)))
  "Returns string type for a service object of type 'ManageModels-response"
  "lstm_motion_model/ManageModelsResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ManageModels-response>)))
  "Returns md5sum for a message object of type '<ManageModels-response>"
  "bdd8f71f894accd0c4b5f9c68c657241")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ManageModels-response)))
  "Returns md5sum for a message object of type 'ManageModels-response"
  "bdd8f71f894accd0c4b5f9c68c657241")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ManageModels-response>)))
  "Returns full string definition for message of type '<ManageModels-response>"
  (cl:format cl:nil "ModelManagement[] management_responses~%~%~%================================================================================~%MSG: lstm_motion_model/ModelManagement~%uint64 id~%uint16 action~%uint16 NEW=0~%uint16 COPY=1~%uint16 DELETE=2~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ManageModels-response)))
  "Returns full string definition for message of type 'ManageModels-response"
  (cl:format cl:nil "ModelManagement[] management_responses~%~%~%================================================================================~%MSG: lstm_motion_model/ModelManagement~%uint64 id~%uint16 action~%uint16 NEW=0~%uint16 COPY=1~%uint16 DELETE=2~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ManageModels-response>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'management_responses) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ManageModels-response>))
  "Converts a ROS message object to a list"
  (cl:list 'ManageModels-response
    (cl:cons ':management_responses (management_responses msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'ManageModels)))
  'ManageModels-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'ManageModels)))
  'ManageModels-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ManageModels)))
  "Returns string type for a service object of type '<ManageModels>"
  "lstm_motion_model/ManageModels")