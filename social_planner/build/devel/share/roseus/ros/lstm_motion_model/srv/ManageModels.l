;; Auto-generated. Do not edit!


(when (boundp 'lstm_motion_model::ManageModels)
  (if (not (find-package "LSTM_MOTION_MODEL"))
    (make-package "LSTM_MOTION_MODEL"))
  (shadow 'ManageModels (find-package "LSTM_MOTION_MODEL")))
(unless (find-package "LSTM_MOTION_MODEL::MANAGEMODELS")
  (make-package "LSTM_MOTION_MODEL::MANAGEMODELS"))
(unless (find-package "LSTM_MOTION_MODEL::MANAGEMODELSREQUEST")
  (make-package "LSTM_MOTION_MODEL::MANAGEMODELSREQUEST"))
(unless (find-package "LSTM_MOTION_MODEL::MANAGEMODELSRESPONSE")
  (make-package "LSTM_MOTION_MODEL::MANAGEMODELSRESPONSE"))

(in-package "ROS")





(defclass lstm_motion_model::ManageModelsRequest
  :super ros::object
  :slots (_management_requests ))

(defmethod lstm_motion_model::ManageModelsRequest
  (:init
   (&key
    ((:management_requests __management_requests) (let (r) (dotimes (i 0) (push (instance lstm_motion_model::ModelManagement :init) r)) r))
    )
   (send-super :init)
   (setq _management_requests __management_requests)
   self)
  (:management_requests
   (&rest __management_requests)
   (if (keywordp (car __management_requests))
       (send* _management_requests __management_requests)
     (progn
       (if __management_requests (setq _management_requests (car __management_requests)))
       _management_requests)))
  (:serialization-length
   ()
   (+
    ;; lstm_motion_model/ModelManagement[] _management_requests
    (apply #'+ (send-all _management_requests :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; lstm_motion_model/ModelManagement[] _management_requests
     (write-long (length _management_requests) s)
     (dolist (elem _management_requests)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; lstm_motion_model/ModelManagement[] _management_requests
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _management_requests (let (r) (dotimes (i n) (push (instance lstm_motion_model::ModelManagement :init) r)) r))
     (dolist (elem- _management_requests)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(defclass lstm_motion_model::ManageModelsResponse
  :super ros::object
  :slots (_management_responses ))

(defmethod lstm_motion_model::ManageModelsResponse
  (:init
   (&key
    ((:management_responses __management_responses) (let (r) (dotimes (i 0) (push (instance lstm_motion_model::ModelManagement :init) r)) r))
    )
   (send-super :init)
   (setq _management_responses __management_responses)
   self)
  (:management_responses
   (&rest __management_responses)
   (if (keywordp (car __management_responses))
       (send* _management_responses __management_responses)
     (progn
       (if __management_responses (setq _management_responses (car __management_responses)))
       _management_responses)))
  (:serialization-length
   ()
   (+
    ;; lstm_motion_model/ModelManagement[] _management_responses
    (apply #'+ (send-all _management_responses :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; lstm_motion_model/ModelManagement[] _management_responses
     (write-long (length _management_responses) s)
     (dolist (elem _management_responses)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; lstm_motion_model/ModelManagement[] _management_responses
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _management_responses (let (r) (dotimes (i n) (push (instance lstm_motion_model::ModelManagement :init) r)) r))
     (dolist (elem- _management_responses)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(defclass lstm_motion_model::ManageModels
  :super ros::object
  :slots ())

(setf (get lstm_motion_model::ManageModels :md5sum-) "bdd8f71f894accd0c4b5f9c68c657241")
(setf (get lstm_motion_model::ManageModels :datatype-) "lstm_motion_model/ManageModels")
(setf (get lstm_motion_model::ManageModels :request) lstm_motion_model::ManageModelsRequest)
(setf (get lstm_motion_model::ManageModels :response) lstm_motion_model::ManageModelsResponse)

(defmethod lstm_motion_model::ManageModelsRequest
  (:response () (instance lstm_motion_model::ManageModelsResponse :init)))

(setf (get lstm_motion_model::ManageModelsRequest :md5sum-) "bdd8f71f894accd0c4b5f9c68c657241")
(setf (get lstm_motion_model::ManageModelsRequest :datatype-) "lstm_motion_model/ManageModelsRequest")
(setf (get lstm_motion_model::ManageModelsRequest :definition-)
      "ModelManagement[] management_requests

================================================================================
MSG: lstm_motion_model/ModelManagement
uint64 id
uint16 action
uint16 NEW=0
uint16 COPY=1
---
ModelManagement[] management_responses


================================================================================
MSG: lstm_motion_model/ModelManagement
uint64 id
uint16 action
uint16 NEW=0
uint16 COPY=1
")

(setf (get lstm_motion_model::ManageModelsResponse :md5sum-) "bdd8f71f894accd0c4b5f9c68c657241")
(setf (get lstm_motion_model::ManageModelsResponse :datatype-) "lstm_motion_model/ManageModelsResponse")
(setf (get lstm_motion_model::ManageModelsResponse :definition-)
      "ModelManagement[] management_requests

================================================================================
MSG: lstm_motion_model/ModelManagement
uint64 id
uint16 action
uint16 NEW=0
uint16 COPY=1
---
ModelManagement[] management_responses


================================================================================
MSG: lstm_motion_model/ModelManagement
uint64 id
uint16 action
uint16 NEW=0
uint16 COPY=1
")



(provide :lstm_motion_model/ManageModels "bdd8f71f894accd0c4b5f9c68c657241")


