import os
import json

from typing import List, Dict, Any

from app import db
from app import settings as config
from app import utils
from app.auth.jwt import get_current_user
from app.model.schema import PredictRequest, PredictResponse
from app.model.services import model_predict
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

router = APIRouter(tags=["Model"], prefix="/model")

@router.post("/predict")
async def predict(data: Dict[str, Any], 
    current_user=Depends(get_current_user)):

    print(f"Processing data {data}, type {type(data)}...") 

    rpse = {"success": False, "prediction": None, "score": None}

    # Send the file to be processed by the model service
    #prediction, score = await model_predict(file_hash)
    prediction, score = await model_predict(data)
    rpse["success"] = True
    rpse["prediction"] = prediction
    rpse["score"] = score
    #rpse["image_file_name"] = file_hash

    # except Exception as e:
    #    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return PredictResponse(**rpse)
