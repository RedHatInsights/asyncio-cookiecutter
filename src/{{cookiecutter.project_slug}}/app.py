import asyncio
import json
import logging
import os
from collections import deque
from contextvars import ContextVar
from functools import partial

from kafkahelpers import make_pair, make_producer
from {{cookiecutter.project_slug}} import metrics

logging.basicConfig(level=logging.INFO)


def context_filter(record):
    record.request_id = REQUEST_ID.get()
    return True


logger = logging.getLogger(__name__)
logger.addFilter(context_filter)

loop = asyncio.get_event_loop()

BOOT = os.environ.get("KAFKAMQ", "kafka:29092").split(",")
GROUP = os.environ.get("GROUP", "{{cookiecutter.project_slug}}")
INBOUND_TOPIC = os.environ.get("QUEUE", "{{cookiecutter.inbound_topic}}")
OUTBOUND_TOPIC = os.environ.get("RESPONSE_QUEUE", "{{cookiecutter.outbound_topic}}")
REQUEST_ID = ContextVar("request_id")
REQUEST_ID.set("-1")

async def consumer(client, produce_queue=None):
    async for msg in client:
        produce_queue.append({"FOO": "BAR", "payload_id": REQUEST_ID.get()})


async def send_item(client, item):
    await client.send_and_wait(OUTBOUND_TOPIC, json.dumps(item).encode("utf-8"))


def main():
    reader, writer = make_pair(INBOUND_TOPIC, GROUP, BOOT)
    produce_queue = deque()
    loop.create_task(reader.run(partial(consumer, produce_queue=produce_queue)))
    c = make_producer(send_item, produce_queue)
    loop.create_task(writer.run(c))
    metrics.start()
    loop.run_forever()


if __name__ == "__main__":
    main()
