import asyncio
import typing

from event import Event
from redis.asyncio import Redis

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# This WS code is inspired by the encode/broadcaster package.
# If something needs to be fixed or changed, look at their GitHub repo.
class DatabaseBroadcaster:
    def __init__(self):
        self._connection = Redis(host='redis', port=6379, db=0)
        self._pubsub = self._connection.pubsub()
        self._ready = asyncio.Event()
        self._queue: asyncio.Queue[Event] = asyncio.Queue()
        self._listener: asyncio.Task[None] | None = None

    async def connect(self) -> None:
        self._listener = asyncio.create_task(self._pubsub_listener())
        await self._pubsub.connect()

    async def disconnect(self) -> None:
        await self._pubsub.aclose()
        await self._connection.aclose()
        if self._listener is not None:
            self._listener.cancel()

    async def subscribe(self, channel: str) -> None:
        if not self._listener:
            self._listener = asyncio.create_task(self._pubsub_listener())

        self._ready.set()
        await self._pubsub.subscribe(channel)

    async def unsubscribe(self, channel: str) -> None:
        await self._pubsub.unsubscribe(channel)

    async def clear(self) -> None:
        self._ready.clear()
        if self._listener is not None:
            self._listener.cancel()
            self._listener = None

    async def publish(self, channel: str, message: typing.Any) -> None:
        await self._connection.publish(channel, message)

    async def next_published(self) -> Event:
        return await self._queue.get()

    async def _pubsub_listener(self) -> None:
        # redis-py does not listen to the pubsub connection if there are no channels subscribed
        # so we need to wait until the first channel is subscribed to start listening
        await self._ready.wait()
        logger.info("AWAITED READY")
        async for message in self._pubsub.listen():
            if message["type"] == "message":
                event = Event(
                    channel=message["channel"].decode(),
                    message=message["data"].decode(),
                )
                await self._queue.put(event)
