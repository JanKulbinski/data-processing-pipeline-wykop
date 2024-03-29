# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf/wykop.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protobuf/wykop.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x14protobuf/wykop.proto\"8\n\x04Post\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61te\x18\x02 \x01(\t\x12\x14\n\x0c\x63omments_num\x18\x03 \x01(\t\" \n\x0fPredictedPluses\x12\r\n\x05value\x18\x01 \x01(\x03\x32\x31\n\x0cModelService\x12!\n\x04Test\x12\x05.Post\x1a\x10.PredictedPluses\"\x00\x62\x06proto3'
)




_POST = _descriptor.Descriptor(
  name='Post',
  full_name='Post',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='Post.text', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='date', full_name='Post.date', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='comments_num', full_name='Post.comments_num', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=80,
)


_PREDICTEDPLUSES = _descriptor.Descriptor(
  name='PredictedPluses',
  full_name='PredictedPluses',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='PredictedPluses.value', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=82,
  serialized_end=114,
)

DESCRIPTOR.message_types_by_name['Post'] = _POST
DESCRIPTOR.message_types_by_name['PredictedPluses'] = _PREDICTEDPLUSES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Post = _reflection.GeneratedProtocolMessageType('Post', (_message.Message,), {
  'DESCRIPTOR' : _POST,
  '__module__' : 'protobuf.wykop_pb2'
  # @@protoc_insertion_point(class_scope:Post)
  })
_sym_db.RegisterMessage(Post)

PredictedPluses = _reflection.GeneratedProtocolMessageType('PredictedPluses', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTEDPLUSES,
  '__module__' : 'protobuf.wykop_pb2'
  # @@protoc_insertion_point(class_scope:PredictedPluses)
  })
_sym_db.RegisterMessage(PredictedPluses)



_MODELSERVICE = _descriptor.ServiceDescriptor(
  name='ModelService',
  full_name='ModelService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=116,
  serialized_end=165,
  methods=[
  _descriptor.MethodDescriptor(
    name='Test',
    full_name='ModelService.Test',
    index=0,
    containing_service=None,
    input_type=_POST,
    output_type=_PREDICTEDPLUSES,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_MODELSERVICE)

DESCRIPTOR.services_by_name['ModelService'] = _MODELSERVICE

# @@protoc_insertion_point(module_scope)
