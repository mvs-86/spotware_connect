import sys
from .OpenApiCommonMessages_pb2 import *
from .OpenApiCommonModelMessages_pb2 import *
from .OpenApiModelMessages_pb2 import *
from .OpenApiMessages_pb2 import *

PROTOBUF_PAYLOAD_NAME_REPLACES = [('Oa', 'OA'), ('HeartbeatEvent', 'ProtoHeartbeatEvent'), ('ErrorRes', 'ProtoErrorRes'),
    ('OAProto', 'OA'), ('ProtoOAGetAccountsByAccessTokenRes', 'ProtoOAGetAccountListByAccessTokenRes')]
PROTOBUF_CLASSES = [obj for obj in dir(sys.modules[__name__]) if obj.startswith('Proto')]

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
    if msg.payloadType not in [ProtoErrorRes().payloadType, ProtoHeartbeatEvent().payloadType] :
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
        payload.clientMsgId = msgid
        return payload
    return ProtoMessage(payload=payload.SerializeToString(), clientMsgId=str(msgid), payloadType=payload.payloadType)

def print(protobuf):
    if not protobuf:
        return 'No Proto/Payload'
    fields = repr(protobuf).replace(': ', '=').split('\n')[:-1]
    return '%s(%s)' % (protobuf.__class__.__name__, ','.join(fields) )

def get_payload_messages():
    return [p for p in PROTOBUF_CLASSES if p.endswith('Req') or p.endswith('Res') or p.endswith('Event')]

__all__ = ["payload_name_to_camel", "from_payloadType", "message_from_bytes",
           "get_payload_messages", "get_payload", "payload_to_message", "print"] + PROTOBUF_CLASSES
