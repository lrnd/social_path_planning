
(cl:in-package :asdf)

(defsystem "lstm_motion_model-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "ModelManagement" :depends-on ("_package_ModelManagement"))
    (:file "_package_ModelManagement" :depends-on ("_package"))
    (:file "State" :depends-on ("_package_State"))
    (:file "_package_State" :depends-on ("_package"))
  ))