# 🔮 Müşteri Kaybı Tahmin API

[![Testler](https://github.com/sumeyyeealtintas/churn-tahmin-api/actions/workflows/test.yml/badge.svg)](https://github.com/sumeyyeealtintas/churn-tahmin-api/actions/workflows/test.yml)

[`musteri-kaybi-tahmini`](https://github.com/sumeyyeealtintas/musteri-kaybi-tahmini) projesinde eğitilen makine öğrenmesi modelini **FastAPI** ile canlı bir servise çeviren proje. Bir müşterinin bilgilerini gönderirsin, aboneliği bırakma olasılığını ve risk seviyesini alırsın.

> Model bir Jupyter dosyasında kalırsa kimse kullanamaz. Bu proje, modelin **uygulamaya nasıl taşındığını** (deployment) gösterir.

## 🧰 Teknolojiler
Python · FastAPI · Pydantic · scikit-learn · joblib · Pytest · Docker

## 🚀 Çalıştırma
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Swagger arayüzü: `http://127.0.0.1:8000/docs`

## 📨 Örnek İstek
```bash
curl -X POST http://127.0.0.1:8000/tahmin \
  -H "Content-Type: application/json" \
  -d '{"abonelik_ay": 3, "sozlesme": "Aylık", "internet_turu": "Fiber",
       "odeme_yontemi": "Elektronik Çek", "aylik_ucret": 110,
       "destek_cagrisi": 5, "ek_hizmet_sayisi": 0}'
```
Cevap:
```json
{"kayip_olasiligi": 0.78, "risk": "yüksek"}
```
Risk seviyeleri: `< 0.25` düşük · `< 0.5` orta · `≥ 0.5` yüksek.

## ✨ Öne Çıkanlar
- Girdiler `Literal` ve sınır kontrolleriyle doğrulanır; hatalı veri `422` döner
- Model ilk istekte yüklenir ve bellekte tutulur
- Model dosyası yoksa `503` döner, `/saglik` ile kontrol edilir
- Testler: risk mantığı, geçerli/geçersiz girdi, riskli müşteri > sadık müşteri

## 🧪 Test ve Docker
```bash
pytest -q
docker build -t churn-api . && docker run -p 8000:8000 churn-api
```

> Veri sentetiktir, amaç yöntemi göstermektir.
