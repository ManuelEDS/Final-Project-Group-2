import os
import json
import redis
import time
import lightgbm as lgb
from lightgbm import LGBMClassifier
import settings

import pandas as pd
import numpy as np
import joblib
#import pickle
import skopt


db = redis.StrictRedis(host=settings.REDIS_IP, port=settings.REDIS_PORT, db=0)

SCALER = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
# Load the scaler from the pickle file
with open(SCALER, "rb") as f:
    scaler = pickle.load(f)

MODEL = os.path.join(os.path.dirname(__file__), 'variables_dict_m5_3_1.pkl')
model = joblib.load(MODEL)


# ======== PREDICTION FUNCTION ========
def predict(str):
    """
    Runs inference using the loaded model. Returns a dict with the prediction result.
    """
    # Convert input string to a dictionary
    fields = json.loads(str)
    values = { k: float(v) for k, v in fields.items()}
    print(f"Input dict {type(values)}: {values}")


    # Scale the input features----------------------------------------------------------
    dict_scaler = {}
    for i in scaler.feature_names_in_:
        dict_scaler[i] = 0.0

    for key, value in values.items():
        if key in dict_scaler:
            dict_scaler[key] = value

    df = pd.DataFrame(dict_scaler, index=[0])
    transformed_data = scaler.transform(df)

    # Convert the transformed data (NumPy array) back into a DataFrame
    scale_data = pd.DataFrame(transformed_data, columns=df.columns).iloc[0].to_dict()
    scale_values = values.copy()

    for key, value in scale_data.items():
        if key in scale_values:
            scale_values[key] = value



    # Process the model----------------------------------------------------------

    # Convert input_dict to a DataFrame
    X_df = pd.DataFrame([scale_values])


    predictions = model['best_model'].predict(X_df)
    y_prods = model['best_model'].predict_proba(X_df)[:, 1]

    y_pred = (y_prods > model['best_f1_threshold']).astype(int)

    return {
        'prediction': int(y_pred[0]),
        'probability': float(y_prods[0])
    }

# ======== REDIS LISTENER (Optional) ========
import json
import time
import settings
import pandas as pd
# from your_ml_module import predict  # your predict() function
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

        print(f"Job ID {job_id}: {result}") 
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
