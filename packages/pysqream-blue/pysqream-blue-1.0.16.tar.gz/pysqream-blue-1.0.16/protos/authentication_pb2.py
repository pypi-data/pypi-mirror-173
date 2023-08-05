# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/authentication.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos import error_pb2 as protos_dot_error__pb2
from protos import client_info_pb2 as protos_dot_client__info__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bprotos/authentication.proto\x12\x1d\x63om.sqream.cloud.generated.v1\x1a\x12protos/error.proto\x1a\x18protos/client_info.proto\"\xaf\x02\n\x0b\x41uthRequest\x12\x0c\n\x04user\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x11\n\ttenant_id\x18\x03 \x01(\t\x12\x10\n\x08\x64\x61tabase\x18\x04 \x01(\t\x12\x11\n\tsource_ip\x18\x05 \x01(\t\x12>\n\x0b\x63lient_info\x18\x06 \x01(\x0b\x32).com.sqream.cloud.generated.v1.ClientInfo\x12S\n\rclient_params\x18\x07 \x03(\x0b\x32<.com.sqream.cloud.generated.v1.AuthRequest.ClientParamsEntry\x1a\x33\n\x11\x43lientParamsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xa4\x01\n\x0c\x41uthResponse\x12\r\n\x05token\x18\x01 \x01(\t\x12\x12\n\ntoken_type\x18\x02 \x01(\t\x12\x10\n\x08\x65xp_time\x18\x03 \x01(\x03\x12\x12\n\ncontext_id\x18\x04 \x01(\t\x12\x33\n\x05\x65rror\x18\x05 \x01(\x0b\x32$.com.sqream.cloud.generated.v1.Error\x12\x16\n\x0esqream_version\x18\x06 \x01(\t2x\n\x15\x41uthenticationService\x12_\n\x04\x41uth\x12*.com.sqream.cloud.generated.v1.AuthRequest\x1a+.com.sqream.cloud.generated.v1.AuthResponseB\x02P\x01\x62\x06proto3')



_AUTHREQUEST = DESCRIPTOR.message_types_by_name['AuthRequest']
_AUTHREQUEST_CLIENTPARAMSENTRY = _AUTHREQUEST.nested_types_by_name['ClientParamsEntry']
_AUTHRESPONSE = DESCRIPTOR.message_types_by_name['AuthResponse']
AuthRequest = _reflection.GeneratedProtocolMessageType('AuthRequest', (_message.Message,), {

  'ClientParamsEntry' : _reflection.GeneratedProtocolMessageType('ClientParamsEntry', (_message.Message,), {
    'DESCRIPTOR' : _AUTHREQUEST_CLIENTPARAMSENTRY,
    '__module__' : 'protos.authentication_pb2'
    # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.AuthRequest.ClientParamsEntry)
    })
  ,
  'DESCRIPTOR' : _AUTHREQUEST,
  '__module__' : 'protos.authentication_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.AuthRequest)
  })
_sym_db.RegisterMessage(AuthRequest)
_sym_db.RegisterMessage(AuthRequest.ClientParamsEntry)

AuthResponse = _reflection.GeneratedProtocolMessageType('AuthResponse', (_message.Message,), {
  'DESCRIPTOR' : _AUTHRESPONSE,
  '__module__' : 'protos.authentication_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.AuthResponse)
  })
_sym_db.RegisterMessage(AuthResponse)

_AUTHENTICATIONSERVICE = DESCRIPTOR.services_by_name['AuthenticationService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'P\001'
  _AUTHREQUEST_CLIENTPARAMSENTRY._options = None
  _AUTHREQUEST_CLIENTPARAMSENTRY._serialized_options = b'8\001'
  _AUTHREQUEST._serialized_start=109
  _AUTHREQUEST._serialized_end=412
  _AUTHREQUEST_CLIENTPARAMSENTRY._serialized_start=361
  _AUTHREQUEST_CLIENTPARAMSENTRY._serialized_end=412
  _AUTHRESPONSE._serialized_start=415
  _AUTHRESPONSE._serialized_end=579
  _AUTHENTICATIONSERVICE._serialized_start=581
  _AUTHENTICATIONSERVICE._serialized_end=701
# @@protoc_insertion_point(module_scope)
