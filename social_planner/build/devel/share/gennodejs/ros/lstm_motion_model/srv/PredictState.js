// Auto-generated. Do not edit!

// (in-package lstm_motion_model.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let State = require('../msg/State.js');

//-----------------------------------------------------------


//-----------------------------------------------------------

class PredictStateRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.input_states = null;
    }
    else {
      if (initObj.hasOwnProperty('input_states')) {
        this.input_states = initObj.input_states
      }
      else {
        this.input_states = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type PredictStateRequest
    // Serialize message field [input_states]
    // Serialize the length for message field [input_states]
    bufferOffset = _serializer.uint32(obj.input_states.length, buffer, bufferOffset);
    obj.input_states.forEach((val) => {
      bufferOffset = State.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type PredictStateRequest
    let len;
    let data = new PredictStateRequest(null);
    // Deserialize message field [input_states]
    // Deserialize array length for message field [input_states]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.input_states = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.input_states[i] = State.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    object.input_states.forEach((val) => {
      length += State.getMessageSize(val);
    });
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lstm_motion_model/PredictStateRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '36a50c31967d681c62b2fabec29bc0bc';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    State[] input_states
    
    ================================================================================
    MSG: lstm_motion_model/State
    uint64 id
    float32[] state
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new PredictStateRequest(null);
    if (msg.input_states !== undefined) {
      resolved.input_states = new Array(msg.input_states.length);
      for (let i = 0; i < resolved.input_states.length; ++i) {
        resolved.input_states[i] = State.Resolve(msg.input_states[i]);
      }
    }
    else {
      resolved.input_states = []
    }

    return resolved;
    }
};

class PredictStateResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.predicted_states = null;
    }
    else {
      if (initObj.hasOwnProperty('predicted_states')) {
        this.predicted_states = initObj.predicted_states
      }
      else {
        this.predicted_states = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type PredictStateResponse
    // Serialize message field [predicted_states]
    // Serialize the length for message field [predicted_states]
    bufferOffset = _serializer.uint32(obj.predicted_states.length, buffer, bufferOffset);
    obj.predicted_states.forEach((val) => {
      bufferOffset = State.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type PredictStateResponse
    let len;
    let data = new PredictStateResponse(null);
    // Deserialize message field [predicted_states]
    // Deserialize array length for message field [predicted_states]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.predicted_states = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.predicted_states[i] = State.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    object.predicted_states.forEach((val) => {
      length += State.getMessageSize(val);
    });
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lstm_motion_model/PredictStateResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '1c9c8326674c06e54fc1202b2ccc1deb';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    State[] predicted_states
    
    ================================================================================
    MSG: lstm_motion_model/State
    uint64 id
    float32[] state
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new PredictStateResponse(null);
    if (msg.predicted_states !== undefined) {
      resolved.predicted_states = new Array(msg.predicted_states.length);
      for (let i = 0; i < resolved.predicted_states.length; ++i) {
        resolved.predicted_states[i] = State.Resolve(msg.predicted_states[i]);
      }
    }
    else {
      resolved.predicted_states = []
    }

    return resolved;
    }
};

module.exports = {
  Request: PredictStateRequest,
  Response: PredictStateResponse,
  md5sum() { return 'def079bdd0ff18cd456b2d37bbf78613'; },
  datatype() { return 'lstm_motion_model/PredictState'; }
};
