"""
This module contains the SubscribeTopic class.
"""

from typing import Any, Callable
from hbmqtt.client import QOS_1
from hbmqtt.session import ApplicationMessage


class SubscribeTopic(object):
    """Details for a topic the translator will subscribe to."""

    def __init__(self,
                 topic: str,
                 on_message: Callable[['SubscribeTopic', ApplicationMessage], None],
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
    def on_message(self) -> Callable[['SubscribeTopic', ApplicationMessage], None]:
        """Called when a message is received."""
        return self._on_message

    def __getitem__(self, index: int) -> Any:
        """Simulates tuple-like response for HBMQTT's subscribe method."""
        if index == 0:
            return self._topic
        elif index == 1:
            return self._qos
        raise NotImplementedError

    def __repr__(self):
        return "<{}: topic={}, qos={}>".format(
            self.__class__.__name__,
            self._topic,
            self._qos,
        )
