"""Müşteri kaybı modelini REST API olarak sunar."""
from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MODEL_YOLU = Path(__file__).resolve().parent.parent / "model" / "kayip_modeli.joblib"

app = FastAPI(
    title="Müşteri Kaybı Tahmin API",
    description="Bir müşterinin aboneliği bırakma olasılığını döndürür.",
    version="1.0.0",
)
_model = None


def modeli_yukle():
    global _model
    if _model is None:
        if not MODEL_YOLU.exists():
            raise HTTPException(503, "Model dosyası bulunamadı")
        _model = joblib.load(MODEL_YOLU)
    return _model


class Musteri(BaseModel):
    abonelik_ay: int = Field(ge=1, le=120, examples=[8])
    sozlesme: Literal["Aylık", "1 Yıllık", "2 Yıllık"]
    internet_turu: Literal["DSL", "Fiber", "Yok"]
    odeme_yontemi: Literal["Kredi Kartı", "Havale", "Elektronik Çek"]
    aylik_ucret: float = Field(ge=0, examples=[95.5])
    destek_cagrisi: int = Field(ge=0, examples=[3])
    ek_hizmet_sayisi: int = Field(ge=0, le=10, examples=[1])


class Tahmin(BaseModel):
    kayip_olasiligi: float
    risk: Literal["düşük", "orta", "yüksek"]


def risk_seviyesi(p: float) -> str:
    return "düşük" if p < 0.25 else "orta" if p < 0.5 else "yüksek"


@app.get("/saglik")
def saglik():
    return {"durum": "ok", "model_hazir": MODEL_YOLU.exists()}


@app.post("/tahmin", response_model=Tahmin)
def tahmin(musteri: Musteri):
    model = modeli_yukle()
    p = float(model.predict_proba(pd.DataFrame([musteri.model_dump()]))[0, 1])
    return Tahmin(kayip_olasiligi=round(p, 4), risk=risk_seviyesi(p))
