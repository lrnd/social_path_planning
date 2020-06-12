; Auto-generated. Do not edit!


(cl:in-package lstm_motion_model-msg)


;//! \htmlinclude ModelManagement.msg.html

(cl:defclass <ModelManagement> (roslisp-msg-protocol:ros-message)
  ((id
    :reader id
    :initarg :id
    :type cl:integer
    :initform 0)
   (action
    :reader action
    :initarg :action
    :type cl:fixnum
    :initform 0))
)

(cl:defclass ModelManagement (<ModelManagement>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ModelManagement>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ModelManagement)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lstm_motion_model-msg:<ModelManagement> is deprecated: use lstm_motion_model-msg:ModelManagement instead.")))

(cl:ensure-generic-function 'id-val :lambda-list '(m))
(cl:defmethod id-val ((m <ModelManagement>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lstm_motion_model-msg:id-val is deprecated.  Use lstm_motion_model-msg:id instead.")
  (id m))

(cl:ensure-generic-function 'action-val :lambda-list '(m))
(cl:defmethod action-val ((m <ModelManagement>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lstm_motion_model-msg:action-val is deprecated.  Use lstm_motion_model-msg:action instead.")
  (action m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<ModelManagement>)))
    "Constants for message type '<ModelManagement>"
  '((:NEW . 0)
    (:COPY . 1)
    (:DELETE . 2))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'ModelManagement)))
    "Constants for message type 'ModelManagement"
  '((:NEW . 0)
    (:COPY . 1)
    (:DELETE . 2))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ModelManagement>) ostream)
  "Serializes a message object of type '<ModelManagement>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 32) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 40) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 48) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 56) (cl:slot-value msg 'id)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'action)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'action)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ModelManagement>) istream)
  "Deserializes a message object of type '<ModelManagement>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 32) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 40) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 48) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 56) (cl:slot-value msg 'id)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'action)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'action)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ModelManagement>)))
  "Returns string type for a message object of type '<ModelManagement>"
  "lstm_motion_model/ModelManagement")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ModelManagement)))
  "Returns string type for a message object of type 'ModelManagement"
  "lstm_motion_model/ModelManagement")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ModelManagement>)))
  "Returns md5sum for a message object of type '<ModelManagement>"
  "77c26195935ca59ed4ca7d03b9e7c474")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ModelManagement)))
  "Returns md5sum for a message object of type 'ModelManagement"
  "77c26195935ca59ed4ca7d03b9e7c474")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ModelManagement>)))
  "Returns full string definition for message of type '<ModelManagement>"
  (cl:format cl:nil "uint64 id~%uint16 action~%uint16 NEW=0~%uint16 COPY=1~%uint16 DELETE=2~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ModelManagement)))
  "Returns full string definition for message of type 'ModelManagement"
  (cl:format cl:nil "uint64 id~%uint16 action~%uint16 NEW=0~%uint16 COPY=1~%uint16 DELETE=2~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ModelManagement>))
  (cl:+ 0
     8
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ModelManagement>))
  "Converts a ROS message object to a list"
  (cl:list 'ModelManagement
    (cl:cons ':id (id msg))
    (cl:cons ':action (action msg))
))
