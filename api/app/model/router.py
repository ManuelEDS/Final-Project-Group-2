import os
from typing import List

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
async def predict(file: UploadFile, current_user=Depends(get_current_user)):
    rpse = {"success": False, "prediction": None, "score": None}
    
    # Check if a file was sent and that the file is an image
    if not file or not utils.allowed_file(file.filename):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File type is not supported.")
    #try:
    
        # Calculate hash and store the image to disk
    file_hash = await utils.get_file_hash(file)
    file_path = os.path.join(config.UPLOAD_FOLDER, file_hash)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Send the file to be processed by the model service
    #prediction, score = await model_predict(file_hash)
    prediction, score = await model_predict(file_path)
    rpse["success"] = True
    rpse["prediction"] = prediction
    rpse["score"] = score
    rpse["image_file_name"] = file_hash

    # except Exception as e:
    #    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return PredictResponse(**rpse)
