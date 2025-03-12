import json
import time
from uuid import uuid4

import redis
from app import settings #"app" was added.

# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
# Connect to Redis
db = redis.StrictRedis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID
    #decode_responses=True
)
# Verify the connection
try:
    db.ping()
    print("Connected to Redis successfully!")
except redis.ConnectionError:
    print("Failed to connect to Redis.")
# db = None

async def model_predict(data):

    print(f"Processing model_predict {data}, type {type(data)}...")
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    image_name : str
        Name for the image uploaded by the user.

    Returns
    -------
    prediction, score : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    prediction = None
    score = None

    # Assign an unique ID for this job and add it to the queue.
    # We need to assing this ID because we must be able to keep track
    # of this particular job across all the services

    # Generate a unique ID for the job
    job_id = str(uuid4())

    # Create the job data
    job_data = {
        "id": job_id,
        "features": data
    }

    # Add the job to the Redis queue
    db.lpush(settings.REDIS_QUEUE, json.dumps(job_data))

    # Loop until getting the answer from the ML service
    while True:
        result = db.get(job_id)
        if result:
            result = json.loads(result)
            prediction = result["prediction"]
            score = result["score"]
            break
        time.sleep(settings.API_SLEEP)

    return prediction, score
