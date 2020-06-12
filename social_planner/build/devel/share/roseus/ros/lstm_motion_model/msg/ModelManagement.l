;; Auto-generated. Do not edit!


(when (boundp 'lstm_motion_model::ModelManagement)
  (if (not (find-package "LSTM_MOTION_MODEL"))
    (make-package "LSTM_MOTION_MODEL"))
  (shadow 'ModelManagement (find-package "LSTM_MOTION_MODEL")))
(unless (find-package "LSTM_MOTION_MODEL::MODELMANAGEMENT")
  (make-package "LSTM_MOTION_MODEL::MODELMANAGEMENT"))

(in-package "ROS")
;;//! \htmlinclude ModelManagement.msg.html


(intern "*NEW*" (find-package "LSTM_MOTION_MODEL::MODELMANAGEMENT"))
(shadow '*NEW* (find-package "LSTM_MOTION_MODEL::MODELMANAGEMENT"))
(defconstant lstm_motion_model::ModelManagement::*NEW* 0)
(intern "*COPY*" (find-package "LSTM_MOTION_MODEL::MODELMANAGEMENT"))
(shadow '*COPY* (find-package "LSTM_MOTION_MODEL::MODELMANAGEMENT"))
(defconstant lstm_motion_model::ModelManagement::*COPY* 1)
(intern "*DELETE*" (find-package "LSTM_MOTION_MODEL::MODELMANAGEMENT"))
(shadow '*DELETE* (find-package "LSTM_MOTION_MODEL::MODELMANAGEMENT"))
(defconstant lstm_motion_model::ModelManagement::*DELETE* 2)
(defclass lstm_motion_model::ModelManagement
  :super ros::object
  :slots (_id _action ))

(defmethod lstm_motion_model::ModelManagement
  (:init
   (&key
    ((:id __id) 0)
    ((:action __action) 0)
    )
   (send-super :init)
   (setq _id (round __id))
   (setq _action (round __action))
   self)
  (:id
   (&optional __id)
   (if __id (setq _id __id)) _id)
  (:action
   (&optional __action)
   (if __action (setq _action __action)) _action)
  (:serialization-length
   ()
   (+
    ;; uint64 _id
    8
    ;; uint16 _action
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint64 _id
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _id (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _id) (= (length (_id . bv)) 2)) ;; bignum
              (write-long (ash (elt (_id . bv) 0) 0) s)
              (write-long (ash (elt (_id . bv) 1) -1) s))
             ((and (class _id) (= (length (_id . bv)) 1)) ;; big1
              (write-long (elt (_id . bv) 0) s)
              (write-long (if (>= _id 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _id s)(write-long (if (>= _id 0) 0 #xffffffff) s)))
     ;; uint16 _action
       (write-word _action s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint64 _id
     
#+(or :alpha :irix6 :x86_64)
      (setf _id (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _id (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; uint16 _action
     (setq _action (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get lstm_motion_model::ModelManagement :md5sum-) "77c26195935ca59ed4ca7d03b9e7c474")
(setf (get lstm_motion_model::ModelManagement :datatype-) "lstm_motion_model/ModelManagement")
(setf (get lstm_motion_model::ModelManagement :definition-)
      "uint64 id
uint16 action
uint16 NEW=0
uint16 COPY=1
uint16 DELETE=2
")



(provide :lstm_motion_model/ModelManagement "77c26195935ca59ed4ca7d03b9e7c474")


