from fastapi.testclient import TestClient

from app.main import app, risk_seviyesi

istemci = TestClient(app)

ORNEK = {
    "abonelik_ay": 3,
    "sozlesme": "Aylık",
    "internet_turu": "Fiber",
    "odeme_yontemi": "Elektronik Çek",
    "aylik_ucret": 110,
    "destek_cagrisi": 5,
    "ek_hizmet_sayisi": 0,
}


def test_risk_seviyeleri():
    assert risk_seviyesi(0.1) == "düşük"
    assert risk_seviyesi(0.3) == "orta"
    assert risk_seviyesi(0.8) == "yüksek"


def test_tahmin_gecerli():
    r = istemci.post("/tahmin", json=ORNEK)
    assert r.status_code == 200
    assert 0 <= r.json()["kayip_olasiligi"] <= 1


def test_riskli_musteri_sadik_musteriden_yuksek():
    sadik = {**ORNEK, "abonelik_ay": 60, "sozlesme": "2 Yıllık", "destek_cagrisi": 0,
             "ek_hizmet_sayisi": 5, "odeme_yontemi": "Kredi Kartı", "internet_turu": "DSL",
             "aylik_ucret": 50}
    riskli = istemci.post("/tahmin", json=ORNEK).json()["kayip_olasiligi"]
    guvenli = istemci.post("/tahmin", json=sadik).json()["kayip_olasiligi"]
    assert riskli > guvenli


def test_gecersiz_girdi_422():
    assert istemci.post("/tahmin", json={**ORNEK, "sozlesme": "Yok"}).status_code == 422
