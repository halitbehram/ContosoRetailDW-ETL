# 🧪 Contoso ETL Projesi

Bu proje, Microsoft'un ContosoRetailDW veritabanı üzerinden veri çekip (`Extract`), temizleyip ve analiz edip (`Transform`), ardından farklı formatlara (`Load`) dışa aktaran bir ETL sürecini otomatikleştirir.

---

## 🚀 Proje Adımları

### 1. Extract (Veri Çekme)
`extract.py` dosyası, `SQL Server` üzerinde bulunan `ContosoRetailDW` veritabanından aşağıdaki tabloları çeker:

- FactSales  
- FactOnlineSales  
- DimCustomer  
- DimProduct  
- DimDate  
- DimStore

### 2. Transform (Veri Dönüştürme)
`transform.py` dosyasında veriler analiz edilir ve şu çıktılar hazırlanır:

- Aylık satış özeti  
- Müşteri yaşam boyu değeri (CLV)  
- En çok satan ürünler (online, fiziksel ve tüm kanallar)  
- Ürün sezonluk satış trendi  
- Mağaza bazlı satış özeti  
- Tekrar eden müşteri oranı  
- Sadece tekrar eden müşterilere ait satış verileri

### 3. Load (Veri Dışa Aktarma)
`load.py` verileri farklı formatlara aktarır:

- `output/csv/` dizinine CSV dosyaları  
- `output/excel/etl_results.xlsx` içine Excel çıktısı (her tablo ayrı sayfada)  
- `output/sqlite/etl_results.sqlite` olarak SQLite veritabanı  
- (İsteğe bağlı) SQL Server’a tekrar yükleme

---

## 🔧 Gereksinimler

Projenin çalışabilmesi için aşağıdaki Python kütüphanelerinin kurulu olması gerekir:

```bash
pip install -r requirements.txt
