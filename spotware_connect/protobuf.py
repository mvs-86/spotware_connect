import sys
from google.protobuf import message
from .messages.OpenApiCommonMessages_pb2 import *
from .messages.OpenApiCommonModelMessages_pb2 import *
from .messages.OpenApiModelMessages_pb2 import *
from .messages.OpenApiMessages_pb2 import *

PROTOBUF_PAYLOAD_NAME_REPLACES = [('Oa', 'OA'),
    ('HeartbeatEvent', 'ProtoHeartbeatEvent'), ('ErrorRes', 'ProtoErrorRes'),
    ('OAProto', 'OA'),
    ('ProtoOAGetAccountsByAccessTokenRes', 'ProtoOAGetAccountListByAccessTokenRes'),
    ('ProtoOAGetTickdataRes', 'ProtoOAGetTickDataRes')
    ]

NAMES = dir(sys.modules[__name__])
PROTOBUF_CLASSES = [obj for obj in NAMES if obj.startswith('Proto')]


def getReqPayloads(): # pragma: no cover
    return [obj for obj in NAMES if obj.startswith('ProtoOA') and obj.endswith('Req')]


def getResPayloads(): # pragma: no cover
    return [obj for obj in NAMES if obj.startswith('ProtoOA') and obj.endswith('Res')]


def getEventPayloads():  # pragma: no cover
    return [obj for obj in NAMES if obj.startswith('ProtoOA') and obj.endswith('Event')]


def payload_name_to_camel(payload_name, replaces=PROTOBUF_PAYLOAD_NAME_REPLACES):
    words = [w.capitalize() for w in payload_name.split('_')]
    name = ''.join(words)
    for r in replaces:
        name = name.replace(r[0], r[1])
    return name


def from_payloadType(payloadType, *enums):
    if not enums:
        enums = [ProtoPayloadType, ProtoOAPayloadType]
    for enum in enums:
        try:
            class_name = payload_name_to_camel(enum.Name(payloadType))
            return getattr(sys.modules[__name__], class_name)
        except ValueError as e:
            pass
    raise ValueError(f'payloadType {payloadType} not found')


def message_from_bytes(buf):
    msg = ProtoMessage()
    msg.ParseFromString(buf)
    msg_real = from_payloadType(msg.payloadType)()
    if msg.payloadType not in [ProtoErrorRes().payloadType, ProtoHeartbeatEvent().payloadType]:
        return msg
    msg_real.ParseFromString(buf)
    return msg_real


def get_payload(proto_message):
    if not hasattr(proto_message, 'payload'):
        return
    payload = from_payloadType(proto_message.payloadType)()
    payload.ParseFromString(proto_message.payload)
    return payload


def payload_to_message(payload, msgid=''):
    if isinstance(payload, ProtoMessage):
        payload.clientMsgId = msgid if payload.clientMsgId else payload.clientMsgId
        return payload
    return ProtoMessage(payload=payload.SerializeToString(), clientMsgId=str(msgid), payloadType=payload.payloadType)


def describe_fields(protobufs):  # pragma: no cover
    module = sys.modules[__name__]
    fields = dict()
    for pb in protobufs:
        if isinstance(pb, message.Message):
            class_ = pb
        else:
            class_ = getattr(module, pb)
        fields[class_.__name__] = {f.name: f for f in class_.DESCRIPTOR.fields}
    return fields

def to_dict(proto, fields=[]):
    if fields:
        return {f[0].name: f[1] for f in proto.ListFields() if f[0].name in fields}

    return {f[0].name: f[1] for f in proto.ListFields()}

__all__ = ["getReqPayloads", "getResPayloads", "getEventPayloads",
            "payload_name_to_camel", "from_payloadType", "message_from_bytes",
           "get_payload", "payload_to_message", "describe_fields"] + PROTOBUF_CLASSES
