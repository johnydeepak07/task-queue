# taskqueue/models.py
from dataclasses import dataclass, field, asdict
from typing import Literal
import json
import time
import uuid

Lane = Literal['cpu', 'io', 'ml']
LANES: list[Lane] = ['cpu', 'io', 'ml']

DEAD_LETTER_STREAM = 'tasks:dead_letter'


def stream_key(lane: Lane) -> str:
    """All lane stream keys are derived here so the naming is never duplicated."""
    return f'tasks:{lane}'


@dataclass
class Task:
    handler: str                      # which function in handlers.py runs this
    lane: Lane = 'cpu'
    payload: dict = field(default_factory=dict)
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    retries: int = 0
    enqueued_at: float = field(default_factory=time.time)

    def to_redis_fields(self) -> dict:
        """
        Redis Streams store flat string→string maps.
        Nested dicts must be serialized before writing.
        """
        return {
            'task_id':     self.task_id,
            'handler':     self.handler,
            'lane':        self.lane,
            'payload':     json.dumps(self.payload),
            'retries':     str(self.retries),
            'enqueued_at': str(self.enqueued_at),
        }

    @classmethod
    def from_redis_fields(cls, fields: dict) -> 'Task':
        return cls(
            task_id=fields['task_id'],
            handler=fields['handler'],
            lane=fields['lane'],
            payload=json.loads(fields['payload']),
            retries=int(fields['retries']),
            enqueued_at=float(fields['enqueued_at']),
        )