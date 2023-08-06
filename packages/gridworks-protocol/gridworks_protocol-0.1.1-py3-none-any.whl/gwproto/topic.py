import dataclasses
from dataclasses import dataclass


@dataclass
class DecodedMQTTTopic:
    src: str = ""
    envelope_type: str = ""
    message_type: str = ""
    remainder: list[str] = dataclasses.field(default_factory=list)


class MQTTTopic:
    """Valid Gridworks MQTT topic is one of:

     - SRC/ENVELOPE_TYPE/MESSAGE_TYPE, for example: 'hw1-isone-ma-boston-scada/gw/snapshot-spaceheat',
        meaning a message from 'hw1-isone-ma-boston-scada', using envelope format 'gw', with message type
        'snapshot-spaceheat'.

     - SRC/ENVELOPE_TYPE, for example: 'hw1-isone-ma-boston-scada/gw',
        meaning a message from 'hw1-isone-ma-boston-scada', using envelope format 'gw'. Message type must be inferred
        the contents of the envelope.

    - ENVELOPE_TYPE, for example: 'gw',
        meaning a message using envelope format 'gw'. Source and message type must be inferred the contents of the
        envelope.

     - SRC/ENVELOPE_TYPE/MESSAGE_TYPE/OTHER/STUFF, for example: 'hw1-isone-ma-boston-scada/gw/snapshot-spaceheat/bla/bla',
        meaning a message from 'hw1-isone-ma-boston-scada', using envelope format 'gw', with message type
        'snapshot-spaceheat', with extra components OTHER and STUFF that may be used by code down-stream code.

    The only valid component separator is '/'.

    '.' is not a valid character inside the mqtt topic. It must be replaced with '-'.

    It is an error for the message type contained inside the envelope to differ from one specified in the topic.
    """

    DOT_REPLACEMENT = "-"
    SEPARATOR = "/"

    @classmethod
    def encode(cls, src: str, envelope_type: str, message_type: str):
        return (
            src + cls.SEPARATOR + envelope_type + cls.SEPARATOR + message_type
        ).replace(".", cls.DOT_REPLACEMENT)

    @classmethod
    def encode_subscription(cls, src: str, envelope_type: str):
        return cls.encode(src, envelope_type, "#")

    @classmethod
    def decode(cls, topic: str) -> DecodedMQTTTopic:
        if not topic:
            raise ValueError("ERROR. Topic must have at least one character")
        topic = topic.replace("-", ".")
        split = topic.split(cls.SEPARATOR)
        if len(split) == 1:
            src = ""
            envelope_type = split[0]
            message_type = ""
        elif len(split) == 2:
            src = split[0]
            envelope_type = split[1]
            message_type = ""
        else:
            src = split[0]
            envelope_type = split[1]
            message_type = split[2]
        return DecodedMQTTTopic(
            src=src,
            envelope_type=envelope_type,
            message_type=message_type,
            remainder=split[3:],
        )
