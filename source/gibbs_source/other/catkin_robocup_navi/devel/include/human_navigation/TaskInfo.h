// Generated by gencpp from file human_navigation/TaskInfo.msg
// DO NOT EDIT!


#ifndef HUMAN_NAVIGATION_MESSAGE_TASKINFO_H
#define HUMAN_NAVIGATION_MESSAGE_TASKINFO_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <human_navigation/ObjectInfo.h>
#include <human_navigation/ObjectInfo.h>

namespace human_navigation
{
template <class ContainerAllocator>
struct TaskInfo_
{
  typedef TaskInfo_<ContainerAllocator> Type;

  TaskInfo_()
    : environment_id()
    , target_objct()
    , objects_info()  {
    }
  TaskInfo_(const ContainerAllocator& _alloc)
    : environment_id(_alloc)
    , target_objct(_alloc)
    , objects_info(_alloc)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _environment_id_type;
  _environment_id_type environment_id;

   typedef  ::human_navigation::ObjectInfo_<ContainerAllocator>  _target_objct_type;
  _target_objct_type target_objct;

   typedef std::vector< ::human_navigation::ObjectInfo_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::human_navigation::ObjectInfo_<ContainerAllocator> >::other >  _objects_info_type;
  _objects_info_type objects_info;




  typedef boost::shared_ptr< ::human_navigation::TaskInfo_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::human_navigation::TaskInfo_<ContainerAllocator> const> ConstPtr;

}; // struct TaskInfo_

typedef ::human_navigation::TaskInfo_<std::allocator<void> > TaskInfo;

typedef boost::shared_ptr< ::human_navigation::TaskInfo > TaskInfoPtr;
typedef boost::shared_ptr< ::human_navigation::TaskInfo const> TaskInfoConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::human_navigation::TaskInfo_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::human_navigation::TaskInfo_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace human_navigation

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'human_navigation': ['/home/emlab/catkin_robocup/src/humannavi_ros/human_navigation/msg'], 'geometry_msgs': ['/opt/ros/indigo/share/geometry_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/indigo/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::human_navigation::TaskInfo_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::human_navigation::TaskInfo_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::human_navigation::TaskInfo_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::human_navigation::TaskInfo_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::human_navigation::TaskInfo_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::human_navigation::TaskInfo_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::human_navigation::TaskInfo_<ContainerAllocator> >
{
  static const char* value()
  {
    return "c6aa36fad94c1df0d1eba67845a17b36";
  }

  static const char* value(const ::human_navigation::TaskInfo_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xc6aa36fad94c1df0ULL;
  static const uint64_t static_value2 = 0xd1eba67845a17b36ULL;
};

template<class ContainerAllocator>
struct DataType< ::human_navigation::TaskInfo_<ContainerAllocator> >
{
  static const char* value()
  {
    return "human_navigation/TaskInfo";
  }

  static const char* value(const ::human_navigation::TaskInfo_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::human_navigation::TaskInfo_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string environment_id\n\
ObjectInfo target_objct\n\
ObjectInfo[] objects_info\n\
\n\
================================================================================\n\
MSG: human_navigation/ObjectInfo\n\
string name\n\
geometry_msgs/Point position\n\
\n\
================================================================================\n\
MSG: geometry_msgs/Point\n\
# This contains the position of a point in free space\n\
float64 x\n\
float64 y\n\
float64 z\n\
";
  }

  static const char* value(const ::human_navigation::TaskInfo_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::human_navigation::TaskInfo_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.environment_id);
      stream.next(m.target_objct);
      stream.next(m.objects_info);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct TaskInfo_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::human_navigation::TaskInfo_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::human_navigation::TaskInfo_<ContainerAllocator>& v)
  {
    s << indent << "environment_id: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.environment_id);
    s << indent << "target_objct: ";
    s << std::endl;
    Printer< ::human_navigation::ObjectInfo_<ContainerAllocator> >::stream(s, indent + "  ", v.target_objct);
    s << indent << "objects_info[]" << std::endl;
    for (size_t i = 0; i < v.objects_info.size(); ++i)
    {
      s << indent << "  objects_info[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::human_navigation::ObjectInfo_<ContainerAllocator> >::stream(s, indent + "    ", v.objects_info[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // HUMAN_NAVIGATION_MESSAGE_TASKINFO_H
