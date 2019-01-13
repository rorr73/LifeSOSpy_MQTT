"""
This module contains the SubscribeTopic class.
"""

from typing import Any, Callable
from paho.mqtt.client import MQTTMessage
from lifesospy_mqtt.const import QOS_1


class SubscribeTopic(object):
    """Details for a topic the translator will subscribe to."""

    def __init__(self,
                 topic: str,
                 on_message: Callable[['SubscribeTopic', MQTTMessage], None],
                 args: Any = None,
                 qos: int = QOS_1):
        self._topic = topic
        self._on_message = on_message
        self._args = args
        self._qos = qos

    @property
    def args(self) -> Any:
        """Arguments that may be relevant when processing message."""
        return self._args

    @property
    def qos(self) -> int:
        """Quality of service."""
        return self._qos

    @property
    def topic(self) -> str:
        """Topic to subscribe to."""
        return self._topic

    @property
    def on_message(self) -> Callable[['SubscribeTopic', MQTTMessage], None]:
        """Called when a message is received."""
        return self._on_message

    def __repr__(self):
        return "<{}: topic={}, qos={}>".format(
            self.__class__.__name__,
            self._topic,
            self._qos,
        )
