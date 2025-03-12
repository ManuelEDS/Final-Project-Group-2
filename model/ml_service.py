import json
import os
import time

import lightgbm as lgb
import pandas as pd
import redis
import settings

db = redis.StrictRedis(host=settings.REDIS_IP, port=settings.REDIS_PORT, db=0)

# ======== LOAD ARTIFACTS ========
# Use relative path to load the pickle model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'lgbm_model.pkl')
loaded_model = lgb.Booster(model_file=MODEL_PATH)

# TOP_FEATURES_PATH = os.path.join(os.path.dirname(__file__), 'top_features.pkl')
# top_features = joblib.load(TOP_FEATURES_PATH)


# ======== PREDICTION FUNCTION ========
def predict(json_str):
    """
    Runs inference using the loaded model. Returns a dict with the prediction result.
    """
    input_dict = json.loads(json_str)
    X_df= pd.DataFrame([input_dict])
    predictions = loaded_model.predict(X_df)
    # Example threshold of 0.3
    y_prods = loaded_model.predict_proba(X_df)[:, 1]
    y_pred = (y_prods > 0.3).astype(int) 
    return {
        "prediction": "You are in fire!",
        "probability": .95
    }


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, take it from the Redis queue, use the loaded ML
    model to get predictions, and store the results back in Redis using
    the original job ID.
    """
    while True:
        # 1. Take a new job from Redis (blocking pop)
        job = db.brpop(settings.REDIS_QUEUE)  
        # job is a tuple (queue_name, job_data_bytes)
        queue_name, job_data_bytes = job

        # 2. Decode the JSON data for the given job
        job_data = json.loads(job_data_bytes)

        # 3. Get and keep the original job ID
        job_id = job_data['id']

        # 4. Prepare input features as a JSON string
        #    e.g., if your job_data has a dict under "features":
        input_features_json = json.dumps(job_data['features'])
        
        # 5. Run the loaded ML model using your predict() function
        #    NOTE: Make sure your predict() references input_df instead of X_test 
        #    for predict_proba if you want real-time inference.
        result = predict(input_features_json)  
        # result should look like {"prediction": <0/1>, "probability": <float>}

        # 6. Prepare a new JSON with the results
        output = {
            "prediction": result['prediction'],
            "score": result['probability']
        }

        # 7. Store the job results on Redis using the original job ID as the key
        db.set(job_id, json.dumps(output))

        # 8. Sleep briefly before checking for next job
        time.sleep(settings.SERVER_SLEEP)


if __name__ == '__main__':
    print("Launching ML Service...")
    # For a simple service that just listens to Redis:
    classify_process()
