
(cl:in-package :asdf)

(defsystem "egpsr-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "EgpsrMsg" :depends-on ("_package_EgpsrMsg"))
    (:file "_package_EgpsrMsg" :depends-on ("_package"))
  ))