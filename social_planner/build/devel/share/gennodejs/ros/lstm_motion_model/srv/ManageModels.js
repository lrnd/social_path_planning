// Auto-generated. Do not edit!

// (in-package lstm_motion_model.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let ModelManagement = require('../msg/ModelManagement.js');

//-----------------------------------------------------------


//-----------------------------------------------------------

class ManageModelsRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.management_requests = null;
    }
    else {
      if (initObj.hasOwnProperty('management_requests')) {
        this.management_requests = initObj.management_requests
      }
      else {
        this.management_requests = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ManageModelsRequest
    // Serialize message field [management_requests]
    // Serialize the length for message field [management_requests]
    bufferOffset = _serializer.uint32(obj.management_requests.length, buffer, bufferOffset);
    obj.management_requests.forEach((val) => {
      bufferOffset = ModelManagement.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ManageModelsRequest
    let len;
    let data = new ManageModelsRequest(null);
    // Deserialize message field [management_requests]
    // Deserialize array length for message field [management_requests]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.management_requests = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.management_requests[i] = ModelManagement.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 10 * object.management_requests.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lstm_motion_model/ManageModelsRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'cb85bd4cb0b6b722cfbf8f8d20812d23';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    ModelManagement[] management_requests
    
    ================================================================================
    MSG: lstm_motion_model/ModelManagement
    uint64 id
    uint16 action
    uint16 NEW=0
    uint16 COPY=1
    uint16 DELETE=2
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ManageModelsRequest(null);
    if (msg.management_requests !== undefined) {
      resolved.management_requests = new Array(msg.management_requests.length);
      for (let i = 0; i < resolved.management_requests.length; ++i) {
        resolved.management_requests[i] = ModelManagement.Resolve(msg.management_requests[i]);
      }
    }
    else {
      resolved.management_requests = []
    }

    return resolved;
    }
};

class ManageModelsResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.management_responses = null;
    }
    else {
      if (initObj.hasOwnProperty('management_responses')) {
        this.management_responses = initObj.management_responses
      }
      else {
        this.management_responses = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ManageModelsResponse
    // Serialize message field [management_responses]
    // Serialize the length for message field [management_responses]
    bufferOffset = _serializer.uint32(obj.management_responses.length, buffer, bufferOffset);
    obj.management_responses.forEach((val) => {
      bufferOffset = ModelManagement.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ManageModelsResponse
    let len;
    let data = new ManageModelsResponse(null);
    // Deserialize message field [management_responses]
    // Deserialize array length for message field [management_responses]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.management_responses = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.management_responses[i] = ModelManagement.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 10 * object.management_responses.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lstm_motion_model/ManageModelsResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9572533ca7487132f8ea8db2279ad42b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    ModelManagement[] management_responses
    
    
    ================================================================================
    MSG: lstm_motion_model/ModelManagement
    uint64 id
    uint16 action
    uint16 NEW=0
    uint16 COPY=1
    uint16 DELETE=2
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ManageModelsResponse(null);
    if (msg.management_responses !== undefined) {
      resolved.management_responses = new Array(msg.management_responses.length);
      for (let i = 0; i < resolved.management_responses.length; ++i) {
        resolved.management_responses[i] = ModelManagement.Resolve(msg.management_responses[i]);
      }
    }
    else {
      resolved.management_responses = []
    }

    return resolved;
    }
};

module.exports = {
  Request: ManageModelsRequest,
  Response: ManageModelsResponse,
  md5sum() { return 'bdd8f71f894accd0c4b5f9c68c657241'; },
  datatype() { return 'lstm_motion_model/ManageModels'; }
};
