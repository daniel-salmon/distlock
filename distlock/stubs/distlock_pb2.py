# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: distlock.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 5, 28, 1, "", "distlock.proto"
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0e\x64istlock.proto\x12\x08\x64istlock"\x0f\n\rEmptyResponse" \n\x11\x43reateLockRequest\x12\x0b\n\x03key\x18\x01 \x01(\t2P\n\x08\x44istlock\x12\x44\n\nCreateLock\x12\x1b.distlock.CreateLockRequest\x1a\x17.distlock.EmptyResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "distlock_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_EMPTYRESPONSE"]._serialized_start = 28
    _globals["_EMPTYRESPONSE"]._serialized_end = 43
    _globals["_CREATELOCKREQUEST"]._serialized_start = 45
    _globals["_CREATELOCKREQUEST"]._serialized_end = 77
    _globals["_DISTLOCK"]._serialized_start = 79
    _globals["_DISTLOCK"]._serialized_end = 159
# @@protoc_insertion_point(module_scope)
