from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from fastapi.responses import Response
import base64
import requests
import pandas as pd
import json
from graphene import ObjectType, String, Int, List, Schema, Mutation, Field
import os
from db_control import crud, mymodels_MySQL
from db_control.create_tables_MySQL import init_db
from dotenv import load_dotenv

app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

##　nakano add start
import base64
from fastapi.responses import Response
##　nakano add end

"""
# # アプリケーション初期化時にテーブルを作成
init_db()

"""

#logger定義
logger = logging.getLogger("uvicorn.error")

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "FastAPI top page!"}

@app.get("/numbers")
def get_numbers():
    return [1, 5, 10, 15, 20]

@app.get("/profile")
def read_dog_profile(dog_id: str = Query(...)):
    result = crud.dogselect(mymodels_MySQL.profile, dog_id)
    if not result:
        raise HTTPException(status_code=404, detail="Dog_profile not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None

@app.get("/recommend_misic")
def read_recommend_misic(dog_id: str = Query(...)):
    result = crud.historyselect(mymodels_MySQL.history_tbl, dog_id)
    if not result:
        raise HTTPException(status_code=404, detail="history_tbl not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None

## add nakano_start

@app.get("/get_misic")
def read_music_tbl(souund_id: str = Query(...)):
    try:
        sound_id_int = int(souund_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid sound_id")

    result = crud.soundselect(mymodels_MySQL.music_tbl, sound_id_int)
    if not result:
        raise HTTPException(status_code=404, detail="souund_id not found")

    result_obj = json.loads(result)
    if not result_obj:
        raise HTTPException(status_code=404, detail="souund_id not found")

    music_data_base64 = result_obj[0]["music_data"]
    try:
        music_data_bytes = base64.b64decode(music_data_base64)
    except Exception as e:
        logger.error(f"Base64 decode error: {e}")
        raise HTTPException(status_code=500, detail="音声データのデコードに失敗しました")

    return Response(content=music_data_bytes, media_type="audio/mpeg")

@app.get("/music/{music_id}")
def get_music_by_path(music_id: str):
    try:
        music_id_int = int(music_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid music_id")

    result = crud.soundselect(mymodels_MySQL.music_tbl, music_id_int)
    if not result:
        raise HTTPException(status_code=404, detail="music_id not found")

    result_obj = json.loads(result)
    if not result_obj:
        raise HTTPException(status_code=404, detail="music_id not found")

    try:
        music_data_bytes = base64.b64decode(result_obj[0]["music_data"])
    except Exception as e:
        logger.error(f"Base64 decode error: {e}")
        raise HTTPException(status_code=500, detail="音声データのデコードに失敗しました")

    return Response(content=music_data_bytes, media_type="audio/mpeg")

## add nakano_end