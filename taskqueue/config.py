# taskqueue/config.py
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_URL  = os.getenv('REDIS_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}')

CONSUMER_GROUP = 'workers'

# How long a task can sit unacknowledged before another worker reclaims it
CLAIM_TIMEOUT_MS = 30_000

MAX_RETRIES = 3