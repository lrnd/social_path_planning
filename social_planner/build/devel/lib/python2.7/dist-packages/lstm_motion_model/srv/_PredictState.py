# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from lstm_motion_model/PredictStateRequest.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import lstm_motion_model.msg

class PredictStateRequest(genpy.Message):
  _md5sum = "36a50c31967d681c62b2fabec29bc0bc"
  _type = "lstm_motion_model/PredictStateRequest"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """State[] input_states

================================================================================
MSG: lstm_motion_model/State
uint64 id
float32[] state"""
  __slots__ = ['input_states']
  _slot_types = ['lstm_motion_model/State[]']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       input_states

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(PredictStateRequest, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.input_states is None:
        self.input_states = []
    else:
      self.input_states = []

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      length = len(self.input_states)
      buff.write(_struct_I.pack(length))
      for val1 in self.input_states:
        buff.write(_get_struct_Q().pack(val1.id))
        length = len(val1.state)
        buff.write(_struct_I.pack(length))
        pattern = '<%sf'%length
        buff.write(struct.pack(pattern, *val1.state))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      if self.input_states is None:
        self.input_states = None
      end = 0
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.input_states = []
      for i in range(0, length):
        val1 = lstm_motion_model.msg.State()
        start = end
        end += 8
        (val1.id,) = _get_struct_Q().unpack(str[start:end])
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        pattern = '<%sf'%length
        start = end
        end += struct.calcsize(pattern)
        val1.state = struct.unpack(pattern, str[start:end])
        self.input_states.append(val1)
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      length = len(self.input_states)
      buff.write(_struct_I.pack(length))
      for val1 in self.input_states:
        buff.write(_get_struct_Q().pack(val1.id))
        length = len(val1.state)
        buff.write(_struct_I.pack(length))
        pattern = '<%sf'%length
        buff.write(val1.state.tostring())
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      if self.input_states is None:
        self.input_states = None
      end = 0
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.input_states = []
      for i in range(0, length):
        val1 = lstm_motion_model.msg.State()
        start = end
        end += 8
        (val1.id,) = _get_struct_Q().unpack(str[start:end])
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        pattern = '<%sf'%length
        start = end
        end += struct.calcsize(pattern)
        val1.state = numpy.frombuffer(str[start:end], dtype=numpy.float32, count=length)
        self.input_states.append(val1)
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_Q = None
def _get_struct_Q():
    global _struct_Q
    if _struct_Q is None:
        _struct_Q = struct.Struct("<Q")
    return _struct_Q
# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from lstm_motion_model/PredictStateResponse.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import lstm_motion_model.msg

class PredictStateResponse(genpy.Message):
  _md5sum = "1c9c8326674c06e54fc1202b2ccc1deb"
  _type = "lstm_motion_model/PredictStateResponse"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """State[] predicted_states

================================================================================
MSG: lstm_motion_model/State
uint64 id
float32[] state"""
  __slots__ = ['predicted_states']
  _slot_types = ['lstm_motion_model/State[]']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       predicted_states

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(PredictStateResponse, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.predicted_states is None:
        self.predicted_states = []
    else:
      self.predicted_states = []

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      length = len(self.predicted_states)
      buff.write(_struct_I.pack(length))
      for val1 in self.predicted_states:
        buff.write(_get_struct_Q().pack(val1.id))
        length = len(val1.state)
        buff.write(_struct_I.pack(length))
        pattern = '<%sf'%length
        buff.write(struct.pack(pattern, *val1.state))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      if self.predicted_states is None:
        self.predicted_states = None
      end = 0
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.predicted_states = []
      for i in range(0, length):
        val1 = lstm_motion_model.msg.State()
        start = end
        end += 8
        (val1.id,) = _get_struct_Q().unpack(str[start:end])
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        pattern = '<%sf'%length
        start = end
        end += struct.calcsize(pattern)
        val1.state = struct.unpack(pattern, str[start:end])
        self.predicted_states.append(val1)
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      length = len(self.predicted_states)
      buff.write(_struct_I.pack(length))
      for val1 in self.predicted_states:
        buff.write(_get_struct_Q().pack(val1.id))
        length = len(val1.state)
        buff.write(_struct_I.pack(length))
        pattern = '<%sf'%length
        buff.write(val1.state.tostring())
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      if self.predicted_states is None:
        self.predicted_states = None
      end = 0
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.predicted_states = []
      for i in range(0, length):
        val1 = lstm_motion_model.msg.State()
        start = end
        end += 8
        (val1.id,) = _get_struct_Q().unpack(str[start:end])
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        pattern = '<%sf'%length
        start = end
        end += struct.calcsize(pattern)
        val1.state = numpy.frombuffer(str[start:end], dtype=numpy.float32, count=length)
        self.predicted_states.append(val1)
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_Q = None
def _get_struct_Q():
    global _struct_Q
    if _struct_Q is None:
        _struct_Q = struct.Struct("<Q")
    return _struct_Q
class PredictState(object):
  _type          = 'lstm_motion_model/PredictState'
  _md5sum = 'def079bdd0ff18cd456b2d37bbf78613'
  _request_class  = PredictStateRequest
  _response_class = PredictStateResponse