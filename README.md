# Nordic Energy Data Platform

## ÖNEMLİ MENTAL MODEL

Şirketlerde bu şöyle işler:

* feature branch → “task çalışması”
* PR → “code review”
* dev → “test ortamı”
* main → “production”


# 06.05.2026 - Yavuz
### 1
- git branch dev
- git checkout dev
- git branch

Bu ne demek?

Artık:

* main = sabit (production gibi)
* dev = geliştirme alanı

# Bundan sonra:

* kod yazarken dev kullanacağız
* main’e direkt dokunmayacağız

### 2 --> Feature branch oluşturma (gerçek iş yapma modeli)
Mantık şu:

* dev = geliştirme alanı
* feature/* = tek bir iş / task

- git branch -> dev'de olduğuna emin ol
- feature branch oluştur -> git checkout -b feature/ingestion-setup

Artık feature içindeki ilk commiti yapacağız

### 08.05.2026 - Ömer
- ingestion modül yapısı oluşturuldu
- raw, scripts, sources ve tests klasörleri eklendi
- Python ve pandas ortam kurulumu yapıldı
- örnek Nordic enerji veri seti oluşturuldu
- pandas kullanılarak ilk ingestion pipeline geliştirildi
- dataframe inceleme ve temel veri doğrulama kontrolleri eklendi
