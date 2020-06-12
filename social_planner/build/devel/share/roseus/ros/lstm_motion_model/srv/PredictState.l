;; Auto-generated. Do not edit!


(when (boundp 'lstm_motion_model::PredictState)
  (if (not (find-package "LSTM_MOTION_MODEL"))
    (make-package "LSTM_MOTION_MODEL"))
  (shadow 'PredictState (find-package "LSTM_MOTION_MODEL")))
(unless (find-package "LSTM_MOTION_MODEL::PREDICTSTATE")
  (make-package "LSTM_MOTION_MODEL::PREDICTSTATE"))
(unless (find-package "LSTM_MOTION_MODEL::PREDICTSTATEREQUEST")
  (make-package "LSTM_MOTION_MODEL::PREDICTSTATEREQUEST"))
(unless (find-package "LSTM_MOTION_MODEL::PREDICTSTATERESPONSE")
  (make-package "LSTM_MOTION_MODEL::PREDICTSTATERESPONSE"))

(in-package "ROS")





(defclass lstm_motion_model::PredictStateRequest
  :super ros::object
  :slots (_input_states ))

(defmethod lstm_motion_model::PredictStateRequest
  (:init
   (&key
    ((:input_states __input_states) (let (r) (dotimes (i 0) (push (instance lstm_motion_model::State :init) r)) r))
    )
   (send-super :init)
   (setq _input_states __input_states)
   self)
  (:input_states
   (&rest __input_states)
   (if (keywordp (car __input_states))
       (send* _input_states __input_states)
     (progn
       (if __input_states (setq _input_states (car __input_states)))
       _input_states)))
  (:serialization-length
   ()
   (+
    ;; lstm_motion_model/State[] _input_states
    (apply #'+ (send-all _input_states :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; lstm_motion_model/State[] _input_states
     (write-long (length _input_states) s)
     (dolist (elem _input_states)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; lstm_motion_model/State[] _input_states
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _input_states (let (r) (dotimes (i n) (push (instance lstm_motion_model::State :init) r)) r))
     (dolist (elem- _input_states)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(defclass lstm_motion_model::PredictStateResponse
  :super ros::object
  :slots (_predicted_states ))

(defmethod lstm_motion_model::PredictStateResponse
  (:init
   (&key
    ((:predicted_states __predicted_states) (let (r) (dotimes (i 0) (push (instance lstm_motion_model::State :init) r)) r))
    )
   (send-super :init)
   (setq _predicted_states __predicted_states)
   self)
  (:predicted_states
   (&rest __predicted_states)
   (if (keywordp (car __predicted_states))
       (send* _predicted_states __predicted_states)
     (progn
       (if __predicted_states (setq _predicted_states (car __predicted_states)))
       _predicted_states)))
  (:serialization-length
   ()
   (+
    ;; lstm_motion_model/State[] _predicted_states
    (apply #'+ (send-all _predicted_states :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; lstm_motion_model/State[] _predicted_states
     (write-long (length _predicted_states) s)
     (dolist (elem _predicted_states)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; lstm_motion_model/State[] _predicted_states
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _predicted_states (let (r) (dotimes (i n) (push (instance lstm_motion_model::State :init) r)) r))
     (dolist (elem- _predicted_states)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(defclass lstm_motion_model::PredictState
  :super ros::object
  :slots ())

(setf (get lstm_motion_model::PredictState :md5sum-) "def079bdd0ff18cd456b2d37bbf78613")
(setf (get lstm_motion_model::PredictState :datatype-) "lstm_motion_model/PredictState")
(setf (get lstm_motion_model::PredictState :request) lstm_motion_model::PredictStateRequest)
(setf (get lstm_motion_model::PredictState :response) lstm_motion_model::PredictStateResponse)

(defmethod lstm_motion_model::PredictStateRequest
  (:response () (instance lstm_motion_model::PredictStateResponse :init)))

(setf (get lstm_motion_model::PredictStateRequest :md5sum-) "def079bdd0ff18cd456b2d37bbf78613")
(setf (get lstm_motion_model::PredictStateRequest :datatype-) "lstm_motion_model/PredictStateRequest")
(setf (get lstm_motion_model::PredictStateRequest :definition-)
      "State[] input_states

================================================================================
MSG: lstm_motion_model/State
uint64 id
---
State[] predicted_states

================================================================================
MSG: lstm_motion_model/State
uint64 id
")

(setf (get lstm_motion_model::PredictStateResponse :md5sum-) "def079bdd0ff18cd456b2d37bbf78613")
(setf (get lstm_motion_model::PredictStateResponse :datatype-) "lstm_motion_model/PredictStateResponse")
(setf (get lstm_motion_model::PredictStateResponse :definition-)
      "State[] input_states

================================================================================
MSG: lstm_motion_model/State
uint64 id
---
State[] predicted_states

================================================================================
MSG: lstm_motion_model/State
uint64 id
")



(provide :lstm_motion_model/PredictState "def079bdd0ff18cd456b2d37bbf78613")


