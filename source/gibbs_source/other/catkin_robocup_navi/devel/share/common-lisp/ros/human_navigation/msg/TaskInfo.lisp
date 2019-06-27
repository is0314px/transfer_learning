; Auto-generated. Do not edit!


(cl:in-package human_navigation-msg)


;//! \htmlinclude TaskInfo.msg.html

(cl:defclass <TaskInfo> (roslisp-msg-protocol:ros-message)
  ((environment_id
    :reader environment_id
    :initarg :environment_id
    :type cl:string
    :initform "")
   (target_objct
    :reader target_objct
    :initarg :target_objct
    :type human_navigation-msg:ObjectInfo
    :initform (cl:make-instance 'human_navigation-msg:ObjectInfo))
   (objects_info
    :reader objects_info
    :initarg :objects_info
    :type (cl:vector human_navigation-msg:ObjectInfo)
   :initform (cl:make-array 0 :element-type 'human_navigation-msg:ObjectInfo :initial-element (cl:make-instance 'human_navigation-msg:ObjectInfo))))
)

(cl:defclass TaskInfo (<TaskInfo>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <TaskInfo>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'TaskInfo)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name human_navigation-msg:<TaskInfo> is deprecated: use human_navigation-msg:TaskInfo instead.")))

(cl:ensure-generic-function 'environment_id-val :lambda-list '(m))
(cl:defmethod environment_id-val ((m <TaskInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader human_navigation-msg:environment_id-val is deprecated.  Use human_navigation-msg:environment_id instead.")
  (environment_id m))

(cl:ensure-generic-function 'target_objct-val :lambda-list '(m))
(cl:defmethod target_objct-val ((m <TaskInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader human_navigation-msg:target_objct-val is deprecated.  Use human_navigation-msg:target_objct instead.")
  (target_objct m))

(cl:ensure-generic-function 'objects_info-val :lambda-list '(m))
(cl:defmethod objects_info-val ((m <TaskInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader human_navigation-msg:objects_info-val is deprecated.  Use human_navigation-msg:objects_info instead.")
  (objects_info m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <TaskInfo>) ostream)
  "Serializes a message object of type '<TaskInfo>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'environment_id))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'environment_id))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'target_objct) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'objects_info))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'objects_info))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <TaskInfo>) istream)
  "Deserializes a message object of type '<TaskInfo>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'environment_id) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'environment_id) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'target_objct) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'objects_info) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'objects_info)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'human_navigation-msg:ObjectInfo))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<TaskInfo>)))
  "Returns string type for a message object of type '<TaskInfo>"
  "human_navigation/TaskInfo")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'TaskInfo)))
  "Returns string type for a message object of type 'TaskInfo"
  "human_navigation/TaskInfo")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<TaskInfo>)))
  "Returns md5sum for a message object of type '<TaskInfo>"
  "c6aa36fad94c1df0d1eba67845a17b36")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'TaskInfo)))
  "Returns md5sum for a message object of type 'TaskInfo"
  "c6aa36fad94c1df0d1eba67845a17b36")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<TaskInfo>)))
  "Returns full string definition for message of type '<TaskInfo>"
  (cl:format cl:nil "string environment_id~%ObjectInfo target_objct~%ObjectInfo[] objects_info~%~%================================================================================~%MSG: human_navigation/ObjectInfo~%string name~%geometry_msgs/Point position~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'TaskInfo)))
  "Returns full string definition for message of type 'TaskInfo"
  (cl:format cl:nil "string environment_id~%ObjectInfo target_objct~%ObjectInfo[] objects_info~%~%================================================================================~%MSG: human_navigation/ObjectInfo~%string name~%geometry_msgs/Point position~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <TaskInfo>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'environment_id))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'target_objct))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'objects_info) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <TaskInfo>))
  "Converts a ROS message object to a list"
  (cl:list 'TaskInfo
    (cl:cons ':environment_id (environment_id msg))
    (cl:cons ':target_objct (target_objct msg))
    (cl:cons ':objects_info (objects_info msg))
))
