// Generated by gencpp from file lstm_motion_model/State.msg
// DO NOT EDIT!


#ifndef LSTM_MOTION_MODEL_MESSAGE_STATE_H
#define LSTM_MOTION_MODEL_MESSAGE_STATE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace lstm_motion_model
{
template <class ContainerAllocator>
struct State_
{
  typedef State_<ContainerAllocator> Type;

  State_()
    : id(0)
    , state()  {
    }
  State_(const ContainerAllocator& _alloc)
    : id(0)
    , state(_alloc)  {
  (void)_alloc;
    }



   typedef uint64_t _id_type;
  _id_type id;

   typedef std::vector<float, typename ContainerAllocator::template rebind<float>::other >  _state_type;
  _state_type state;





  typedef boost::shared_ptr< ::lstm_motion_model::State_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::lstm_motion_model::State_<ContainerAllocator> const> ConstPtr;

}; // struct State_

typedef ::lstm_motion_model::State_<std::allocator<void> > State;

typedef boost::shared_ptr< ::lstm_motion_model::State > StatePtr;
typedef boost::shared_ptr< ::lstm_motion_model::State const> StateConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::lstm_motion_model::State_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::lstm_motion_model::State_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace lstm_motion_model

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'lstm_motion_model': ['/home/sean/PycharmProjects/human-motion-rnn/lstm_motion_model/msg'], 'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::lstm_motion_model::State_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::lstm_motion_model::State_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::lstm_motion_model::State_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::lstm_motion_model::State_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::lstm_motion_model::State_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::lstm_motion_model::State_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::lstm_motion_model::State_<ContainerAllocator> >
{
  static const char* value()
  {
    return "e91dee59ac98491e7dd0d9122a718840";
  }

  static const char* value(const ::lstm_motion_model::State_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xe91dee59ac98491eULL;
  static const uint64_t static_value2 = 0x7dd0d9122a718840ULL;
};

template<class ContainerAllocator>
struct DataType< ::lstm_motion_model::State_<ContainerAllocator> >
{
  static const char* value()
  {
    return "lstm_motion_model/State";
  }

  static const char* value(const ::lstm_motion_model::State_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::lstm_motion_model::State_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint64 id\n"
"float32[] state\n"
;
  }

  static const char* value(const ::lstm_motion_model::State_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::lstm_motion_model::State_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.id);
      stream.next(m.state);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct State_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::lstm_motion_model::State_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::lstm_motion_model::State_<ContainerAllocator>& v)
  {
    s << indent << "id: ";
    Printer<uint64_t>::stream(s, indent + "  ", v.id);
    s << indent << "state[]" << std::endl;
    for (size_t i = 0; i < v.state.size(); ++i)
    {
      s << indent << "  state[" << i << "]: ";
      Printer<float>::stream(s, indent + "  ", v.state[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // LSTM_MOTION_MODEL_MESSAGE_STATE_H