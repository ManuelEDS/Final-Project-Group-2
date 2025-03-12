import os
import json
import redis
import time
#import joblib
#import lightgbm as lgb
#from lightgbm import LGBMClassifier
import settings

db = redis.StrictRedis(host=settings.REDIS_IP, port=settings.REDIS_PORT, db=0)

# Eliminado, no funciona
#loaded_model = lgb.Booster(model_file='lgbm_model.pkl')


# ======== LOAD ARTIFACTS ========
# Use relative path to load the pickle model
#MODEL_PATH = os.path.join(os.path.dirname(__file__), 'lgbm_model.pkl')
#model = joblib.load(MODEL_PATH)

# (Optional) If you have top_features, scalers, etc.:
# TOP_FEATURES_PATH = os.path.join(os.path.dirname(__file__), 'top_features.pkl')
# top_features = joblib.load(TOP_FEATURES_PATH)


# ======== PREDICTION FUNCTION ========
def predict(json_str):
    """
    Runs inference using the loaded model. Returns a dict with the prediction result.
    """
    return {
        "prediction": "You are in fire!",
        "probability": .95
    }


# ======== REDIS LISTENER (Optional) ========
import json
import time
import settings
import pandas as pd
#from your_ml_module import predict  # your predict() function
# 'loaded_model' is presumably imported or accessible inside predict()

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
