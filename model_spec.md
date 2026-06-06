# Eğitim İçgörü Motoru (EIM) — Model Spec

Amaç

- Platform içi `AI Mentor` ve uyarlanabilir öğrenme özellikleri için öğrenci bilgi düzeyini tahmin etmek, içerik önerileri üretmek ve değerlendirme/özetleme işlerini destekleyecek bir yapay zeka çekirdeği tasarlamak.

Özet (yüksek seviyede)

- Konuşma/özetleme: Hazır bir büyük dil modelini (LLM) servis olarak kullanın; istem-mühendisliği ile eğitim özelinde rehberlik, özet ve soru üretin.

- Öğrenci modelleme (çekirdek): "Eğitim İçgörü Motoru" içinde başlangıç olarak Rasch/IRT (1PL) tabanlı bir öğrenci-yetenek modeli sağlar. İleri seviye için DKT/AKT (LSTM/Transformer) önerilir.

- İçerik önerisi: IRT tahminlerini kullanarak, beklenen kazanım veya bilgi kazancı (expected information gain) hesaplayan seçim algoritması (contextual bandit veya greedy EIG başlangıç için).

- Otomatik değerlendirme: Çoktan seçmeli için IRT; açık uçlu cevaplar için embedding benzerliği (SBERT) veya ince ayarlanmış sınıflandırıcı/puanlayıcı.

Prototype (bu repo)

- `irt_model.py` — kolay okunur, NumPy ile yazılmış Rasch/IRT (1PL) modeli. Çevrimiçi güncelleme ve toplu eğitim yetenekleri içerir.

- `train_irt.py` — sentetik veri üretir, modeli eğitir ve yetenek/difficulty tahminlerinin RMSE değerlerini gösterir.

Veri gereksinimleri

- Öğrenci kimliği, içerik/öğe kimliği, yanıt (0/1), zaman damgası, opsiyonel ödev metni/cevap metni.

- Öğrenci özellikleri (yaş, seviye) ve içerik meta verileri (konu, zorluk) önerilir.

Değerlendirme metrikleri

- Knowledge tracing: AUC, Accuracy, RMSE (theta), Brier score, kalibrasyon eğrileri.

- Öneri sıralaması: NDCG, MAP, ortalama kazanım.

- Otomatik değerlendirme: rubric uyumu (F1), insan-otomatik korelasyonu.

Dağıtım & Online öğrenme

- Model mikroservis olarak sunulmalı (örn. FastAPI), öğrenci cevapları geldikçe çevrimiçi veya minibatch ile güncelleme yapılmalı.

- LLM istekleri ayrı bir servis/kuvvet bağlamında olur; hassas öğrenci verileri maskelenmeli/anonimleştirilmeli.

Geliştirme yol haritası

1. Bu basit IRT prototipini çalıştırın (`train_irt.py`).

2. Gerçek verilerle IRT'yi doğrulayın, ardından DKT/AKT prototipi ekleyin.

3. Öneri katmanını (EIG veya contextual bandit) entegre edin.

4. LLM entegrasyonu ve otomatik değerlendirme eklensin.

Not: Aşağıdaki dosyalar demo amaçlı basit, eğitim amaçlı referans olarak eklendi.
