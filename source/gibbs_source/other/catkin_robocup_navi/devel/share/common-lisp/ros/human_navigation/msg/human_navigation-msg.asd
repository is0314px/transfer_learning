
(cl:in-package :asdf)

(defsystem "human_navigation-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
)
  :components ((:file "_package")
    (:file "ObjectInfo" :depends-on ("_package_ObjectInfo"))
    (:file "_package_ObjectInfo" :depends-on ("_package"))
    (:file "TaskInfo" :depends-on ("_package_TaskInfo"))
    (:file "_package_TaskInfo" :depends-on ("_package"))
    (:file "HumanNaviMsg" :depends-on ("_package_HumanNaviMsg"))
    (:file "_package_HumanNaviMsg" :depends-on ("_package"))
  ))